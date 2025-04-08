# SentimentalSocial_V2

**SentimentalSocial_V2** es una aplicación desarrollada con **FastAPI** que permite analizar el sentimiento de publicaciones en redes sociales de forma rápida y eficiente. La API está diseñada para ser escalable y fácilmente adaptable a cualquier tipo de integración con proyectos externos.

---

## Características

- **Análisis de sentimiento**: La API detecta si el sentimiento de un texto es **positivo**, **negativo** o **neutral**, utilizando algoritmos avanzados de análisis.
- **Documentación interactiva**: Descubre y prueba los endpoints fácilmente mediante la interfaz **Swagger UI** en `/docs` y **ReDoc** en `/redoc`.
- **Arquitectura RESTful**: Perfecto para integraciones con aplicaciones web o clientes front-end.
- **Escalabilidad y rendimiento**: Construida sobre **FastAPI**, con alto rendimiento y potencial para manejo de grandes volúmenes de datos.
- **Soporte para MongoDB**: Almacén de datos eficiente, implementado mediante **Beanie ODM**.

---

## Requisitos previos

Asegúrate de cumplir con los siguientes requisitos antes de instalar el proyecto:

1. **Python 3.8 o superior**.
2. Tener instalado `pip` para manejar paquetes.
3. Tener configurada una base de datos MongoDB (puedes usar MongoDB Atlas o una instancia local).
4. Archivo `.env` para las configuraciones del entorno (como conexión a MongoDB).

---

## Instalación

Sigue estos pasos para instalar y configurar este proyecto en tu máquina local:

### 1. Clona este repositorio

```bash
git clone https://github.com/tu_usuario/sentimentalSocial_V2.git
```

### 2. Navega al directorio del proyecto

```bash
cd sentimentalSocial_V2
```

### 3. Crea un entorno virtual (opcional, pero recomendado)

```bash
python -m venv venv
```

- Activa el entorno virtual:
  - En Windows:
    ```bash
    venv\Scripts\activate
    ```
  - En Linux/macOS:
    ```bash
    source venv/bin/activate
    ```

### 4. Instala las dependencias necesarias

```bash
pip install -r requirements.txt
```

### 5. Configura las variables de entorno

Crea un archivo `.env` en el directorio principal basado en las configuraciones necesarias de la aplicación. Ejemplo:

```env
MONGO_URI=mongodb://localhost:27017/mi_base_de_datos
SECRET_KEY=mi_llave_secreta
```

> **Nota**: Asegúrate de personalizar el archivo `.env` con tus credenciales reales y configure el acceso a tu base de datos MongoDB.

---

## Uso

### 1. Inicia el servidor

Ejecuta el siguiente comando en tu terminal:

```bash
uvicorn app.main:app --reload
```

### 2. Accede a la documentación interactiva

Una vez que el servidor esté ejecutándose, puedes explorar la documentación API en los siguientes enlaces:

- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

**Nota**: Por defecto, el servidor se ejecutará en `http://127.0.0.1:8000`. Si necesitas cambiar el puerto, usa el parámetro `--port` con `uvicorn`, por ejemplo:

```bash
uvicorn app.main:app --reload --port 8080
```

---

## Estructura del proyecto

## Este proyecto sigue una estructura modular para garantizar la escalabilidad y facilidad de mantenimiento.

## Contribuciones

¡Las contribuciones son bienvenidas! Puedes ayudar mejorando el código, añadiendo pruebas o simplemente reportando bugs.

### Cómo contribuir:

1. Crea un fork del repositorio.
2. Haz tus cambios en una nueva rama:
   ```bash
   git checkout -b mi-nueva-rama
   ```
3. Asegúrate de que tu código pase las pruebas (usa `pytest`).
4. Abre un pull request describiendo tus cambios.

---

## FAQ (Preguntas frecuentes)

### 1. **¿Qué hacer si aparece un error al conectarse a MongoDB?**

Asegúrate de que el URI de conexión configurado en tu archivo `.env` sea correcto. Por ejemplo:

```env
MONGO_URI=mongodb://localhost:27017/mi_base_de_datos
```

### 2. **Error: `ModuleNotFoundError` al ejecutar `uvicorn`.**

Esto significa que no has instalado correctamente las dependencias. Asegúrate de ejecutar:

```bash
pip install -r requirements.txt
```

---

## Licencia

Este proyecto está bajo la licencia MIT. Consulta el archivo `LICENSE` para más información.
