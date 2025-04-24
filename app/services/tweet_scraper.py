import asyncio
import logging
import os
from datetime import datetime, timedelta
from random import randint

from twikit import Client, TooManyRequests
from pymongo.errors import PyMongoError
from app.models.tweet import TweetAnalysis, SentimentLabel

# Número mínimo de tweets por defecto
MINIMUM_TWEETS = 500

async def get_authenticated_client() -> Client:
    """
    Obtiene un cliente autenticado de X (antes Twitter).
    Intenta cargar cookies existentes y validar sesión;
    si fallan, hace login y guarda nuevas cookies.
    """
    client = Client(language='en-US')
    username = os.getenv('USERNAME')
    email = os.getenv('EMAIL')
    password = os.getenv('PASSWORD')

    try:
        client.load_cookies('cookies.json')
        # Prueba sencilla para validar
        await client.search_tweet("test", product='Latest', count=1)
        logging.info("Cookies válidas: sesión activa.")
    except Exception:
        await client.login(auth_info_1=username, auth_info_2=email, password=password)
        client.save_cookies('cookies.json')
        logging.info("Login realizado y cookies guardadas.")

    return client

async def get_tweets_page(client: Client, iterator, query: str):
    """
    Obtiene un lote de tweets según iterator:
    - Si iterator es None, hace la búsqueda inicial.
    - En caso contrario, espera y pide la siguiente página.
    """
    if iterator is None:
        logging.info(f"{datetime.now()} - Solicitud inicial de tweets...")
        return await client.search_tweet(query, product='Latest', count=80)
    else:
        delay = randint(3, 8)
        logging.info(f"{datetime.now()} - Esperando {delay}s antes de siguiente página...")
        await asyncio.sleep(delay)
        return await iterator.next()

async def scrape_tweets(query: str, min_tweets: int = MINIMUM_TWEETS):
    """
    Scrapea tweets basados en la query y los guarda en MongoDB
    con estado neutral de sentimiento (score=0.0).
    Devuelve lista de dicts con número, usuario y texto.
    """
    # Definir rango de fechas
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=17)).strftime('%Y-%m-%d')
    search_query = f'{query} lang:en until:{end_date} since:{start_date}'

    client = await get_authenticated_client()
    iterator = None
    tweet_count = 0
    results = []

    while tweet_count < min_tweets:
        try:
            iterator = await get_tweets_page(client, iterator, search_query)
            if not iterator:
                logging.info(f"{datetime.now()} - No se encontraron más tweets.")
                break

            for tweet in iterator:
                tweet_count += 1
                # Guardar documento en MongoDB
                doc = TweetAnalysis(
                    query=query,
                    content=tweet.text,
                    user=tweet.user.screen_name,
                    sentiment_label=SentimentLabel.NEUTRAL,
                    sentiment_score=0.0,
                    processed=False
                )
                try:
                    await doc.insert()
                except PyMongoError as e:
                    logging.error(f"Error insertando en DB: {e}")
                    continue

                results.append({
                    "number": tweet_count,
                    "user": tweet.user.screen_name,
                    "text": tweet.text
                })

                if tweet_count >= min_tweets:
                    break

        except TooManyRequests as e:
            reset = datetime.fromtimestamp(e.rate_limit_reset)
            logging.warning(f"Rate limit alcanzado. Pausando hasta {reset}...")
            await asyncio.sleep(60)
            continue
        except Exception as e:
            logging.error(f"Error inesperado durante scraping: {e}")
            break

    logging.info(f"{datetime.now()} - Scraping completado: {tweet_count} tweets.")
    return results
