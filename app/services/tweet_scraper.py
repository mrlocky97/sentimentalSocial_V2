import asyncio
from datetime import datetime, timedelta
import os
from random import randint

from twikit import Client, TooManyRequests

MINIMUM_TWEETS = 500  # Valor por defecto, pero se puede parametrizar

"""
Obtiene un cliente autenticado.
Intenta cargar cookies previamente guardadas y valida la sesión.
Si falla la validación, realiza login y guarda las nuevas cookies.
"""
async def get_authenticated_client() -> Client:
    client = Client(language='en-US')
    username:str = os.getenv('USERNAME')
    email:str = os.getenv('EMAIL')
    password:str = os.getenv('PASSWORD')

    try:
        client.load_cookies('cookies.json')
        # Realiza una petición de prueba para verificar que las cookies son válidas.
        # Usamos un query sencillo para evitar efectos secundarios.
        test_tweets = await client.search_tweet("test", product='Latest', count=1)
        # Si se llega aquí, se asume que la sesión es válida.
        print(f'{datetime.now()} - Cookies válidas, sesión activa.')
    except Exception as e:
        print(f'{datetime.now()} - Cookies no válidas o error en validación: {e}')
        # Se realiza el login y se guardan las nuevas cookies
        await client.login(auth_info_1=username, auth_info_2=email, password=password)
        client.save_cookies('cookies.json')
        print(f'{datetime.now()} - Se ha realizado el login y se han guardado las nuevas cookies.')
    return client

"""
Función asíncrona para obtener tweets.  
Si 'tweets' es None, se realiza la búsqueda inicial,  
en caso contrario, se espera un tiempo aleatorio y se obtiene el siguiente lote.
"""
async def get_tweets(client, tweets, query: str):
    if tweets is None:
        print(f'{datetime.now()} - Getting tweets...')
        tweets = await client.search_tweet(
            query,
            product='Latest',  # Prioriza tweets recientes
            count=80  # Máximo permitido por solicitud
        )
    else:
        wait_time = randint(3, 8)
        print(f'{datetime.now()} - Getting next tweets after {wait_time} seconds...')
        await asyncio.sleep(wait_time)  # Usamos asyncio.sleep para no bloquear
        tweets = await tweets.next()
    return tweets

"""
Realiza el scraping de tweets usando el hashtag o consulta dada.
Ajusta las fechas de búsqueda y retorna una lista de diccionarios con los tweets.
"""
async def scrape_tweets(query: str, min_tweets: int = MINIMUM_TWEETS):
    # Definir fechas para la búsqueda
    end_date = datetime.now().strftime('%Y-%m-%d')
    start_date = (datetime.now() - timedelta(days=17)).strftime('%Y-%m-%d')
    # Se arma la query incluyendo filtros de idioma y fechas
    search_query = f'{query} lang:en until:{end_date} since:{start_date}'

    # Obtener el cliente autenticado, evitando logins innecesarios
    client = await get_authenticated_client()

    tweet_count = 0
    tweets_iterator = None
    tweets_list = []

    while tweet_count < min_tweets:
        try:
            tweets_iterator = await get_tweets(client, tweets_iterator, search_query)
            if not tweets_iterator:
                print(f'{datetime.now()} - No more tweets found')
                break

            batch_size = len(tweets_iterator)
            for tweet in tweets_iterator:
                tweet_count += 1
                tweet_data = {
                    "number": tweet_count,
                    "user": tweet.user.screen_name,
                    "text": tweet.text
                }
                tweets_list.append(tweet_data)
                if tweet_count >= min_tweets:
                    break

            print(f'{datetime.now()} - Batch: {batch_size} | Total: {tweet_count}')

        except TooManyRequests as e:
            rate_limit_reset = datetime.fromtimestamp(e.rate_limit_reset)
            print(f'{datetime.now()} - Rate limit reached. Waiting until {rate_limit_reset}')
            await asyncio.sleep(60)
            continue

        except Exception as e:
            print(f'{datetime.now()} - Error: {str(e)}')
            break

    print(f'{datetime.now()} - Done! Collected {tweet_count} tweets')
    return tweets_list
