import asyncio
import os
import random
from datetime import datetime, timedelta
from fake_useragent import UserAgent
from twikit import Client, TooManyRequests
import logging

logger = logging.getLogger(__name__)
MIN_TWEETS_PER_BATCH = 10  # Reducido para evitar detección
MAX_WAIT_SECONDS = 600     # 10 minutos máximo de espera

class TwitterScraper:
    def __init__(self):
        self.ua = UserAgent()
        self.proxies = [
            # Lista de proxies (ej: 'http://user:pass@ip:port')
            # Rotar proxies premium aquí para producción
        ]
    
    async def _get_client(self) -> Client:
        """Crea cliente con configuración anti-detección"""
        client = Client(
            language='en-US',
            headers={'User-Agent': self.ua.random},
            proxies={'http': random.choice(self.proxies)} if self.proxies else None
        )
        
        if os.path.exists('cookies.json'):
            try:
                client.load_cookies('cookies.json')
                return client
            except Exception as e:
                logger.warning("Cookies corruptas: %s", str(e))
        
        await self._perform_login(client)
        return client

    async def _perform_login(self, client: Client):
        """Login con reintentos y delays de seguridad"""
        credentials = {
            'auth_info_1': os.getenv('TWITTER_USERNAME'),
            'auth_info_2': os.getenv('TWITTER_EMAIL'),
            'password': os.getenv('TWITTER_PASSWORD')
        }
        
        for attempt in range(3):
            try:
                await client.login(**credentials)
                client.save_cookies('cookies.json')
                logger.info("Login exitoso (Intento %d/3)", attempt+1)
                return
            except Exception as e:
                wait = 2 ** attempt * 60  # Backoff exponencial
                logger.warning("Error en login: %s. Reintento en %ds", str(e), wait)
                await asyncio.sleep(wait)
        
        raise RuntimeError("No se pudo autenticar en Twitter")

    async def scrape_tweets(self, query: str, max_tweets: int) -> list:
        """Scraping seguro con gestión avanzada de rate limits"""
        client = await self._get_client()
        search_query = f"{query} lang:en until:{datetime.now().strftime('%Y-%m-%d')} since:{(datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')}"
        
        tweets = []
        cursor = None
        retries = 0
        
        while len(tweets) < max_tweets:
            try:
                response = await client.search_tweet(
                    search_query,
                    product='Latest',
                    count=MIN_TWEETS_PER_BATCH,
                    cursor=cursor
                )
                
                # Simula interacción humana
                await asyncio.sleep(random.uniform(1, 5))
                
                batch = [{
                    "id": tweet.id,
                    "text": tweet.text,
                    "user": tweet.user.screen_name,
                    "created_at": tweet.created_at
                } for tweet in response]
                
                tweets.extend(batch)
                logger.info("Lote obtenido: %d tweets", len(batch))
                
                if not response.has_next():
                    break
                
                cursor = response.next_cursor
                retries = 0  # Resetear reintentos tras éxito

            except TooManyRequests as e:
                retries += 1
                if retries > 3:
                    logger.error("Bloqueo persistente. Abortando...")
                    break
                
                wait_time = min(2 ** retries * 60, MAX_WAIT_SECONDS)
                logger.warning("Rate limit detectado. Esperando %d segundos", wait_time)
                await asyncio.sleep(wait_time)

            except Exception as e:
                logger.error("Error crítico: %s", str(e), exc_info=True)
                await asyncio.sleep(300)  # Espera larga ante errores inesperados
                continue

        logger.info("Scraping completado. Total: %d tweets", len(tweets))
        return tweets[:max_tweets]  # Asegura no exceder el límite