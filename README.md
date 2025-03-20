# SentimentalSocial_V2

SentimentalSocial_V2 es una aplicación desarrollada con FastAPI que permite analizar el sentimiento de publicaciones en redes sociales.

## Características

- **Análisis de sentimiento**: Detecta si el sentimiento de un texto es positivo, negativo o neutral.
- **API REST**: Endpoints diseñados para interactuar con la aplicación.
- **Escalabilidad**: Construido con FastAPI para un rendimiento óptimo.

## Requisitos previos

- Python 3.8 o superior
- FastAPI
- Uvicorn
- Bibliotecas adicionales (ver `requirements.txt`)

## Instalación

1. Clona este repositorio:
   ```bash
   git clone https://github.com/tu_usuario/sentimentalSocial_V2.git
   ```
2. Navega al directorio del proyecto:
   ```bash
   cd sentimentalSocial_V2
   ```
3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

## Uso

1. Ejecuta el servidor:
   ```bash
   uvicorn main:app --reload
   ```
2. Accede a la documentación interactiva en [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

## Contribuciones

¡Las contribuciones son bienvenidas! Por favor, abre un issue o envía un pull request.

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.
