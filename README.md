# SentimentalSocial_V2

**SentimentalSocial_V2** es una aplicación desarrollada con **FastAPI** que permite analizar el sentimiento de publicaciones en redes sociales de forma rápida y eficiente. La API está diseñada para ser escalable y fácilmente adaptable a cualquier tipo de integración con proyectos externos.

---

## Características

- **Análisis de sentimiento**: Detecta si el sentimiento de un texto es **positivo**, **negativo** o **neutral** con modelos avanzados de NLP.
- **Documentación interactiva**: Prueba los endpoints con **Swagger UI** (`/docs`) y **ReDoc** (`/redoc`).
- **Arquitectura RESTful**: Ideal para integraciones con aplicaciones web o móviles.
- **Escalabilidad y rendimiento**: Basada en **FastAPI** y Beanie ODM sobre MongoDB.
- **Soporte para MongoDB**: Almacenamiento eficiente usando **Beanie** y **Motor**.
- **Autenticación JWT**: Manejo de usuarios y autenticación basada en roles.
- **Notebooks de experimentación**: Incluye notebooks en Jupyter para entrenamiento y evaluación de modelos de sentimiento utilizando `transformers`, `scikit-learn`, etc.

---

## Requisitos previos

1. **Python 3.8 o superior**.
2. Tener instalado `pip`.
3. MongoDB (Atlas o local).
4. Archivo `.env` en la raíz del proyecto con las variables necesarias.
5. (Opcional) GPU y drivers CUDA para acelerar notebooks de entrenamiento.

---

## Instalación

### 1. Clona este repositorio

```bash
git clone https://github.com/tu_usuario/sentimentalSocial_V2.git
cd sentimentalSocial_V2
```

### 2. (Opcional) Crea un entorno virtual

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate
```

### 3. Instala las dependencias principales

```bash
pip install -r requirements.txt
```

### 4. (Opcional) Instala dependencias para notebooks

Si deseas ejecutar los notebooks de entrenamiento y análisis, instala los paquetes extra:

```bash
pip install -r requirements-notebooks.txt
```

### 5. Configura las variables de entorno

Crea un archivo `.env` con contenido similar a:

```env
MONGO_URI=mongodb://localhost:27017/mi_base_de_datos
SECRET_KEY=mi_llave_secreta
```

---

## Uso

### 1. Inicia el servidor API

```bash
uvicorn app.main:app --reload
```

- Accede a Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- Accede a ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

Para cambiar el puerto:

```bash
uvicorn app.main:app --reload --port 8080
```

### 2. Ejecuta los notebooks

Abre Jupyter Lab o Jupyter Notebook desde la raíz del proyecto:

```bash
jupyter lab
# o
jupyter notebook
```

---

## Estructura del proyecto

- `app/`: Código fuente de la API (FastAPI)
- `notebooks/`: Notebooks de experimentación y entrenamiento de modelos
- `requirements.txt`: Dependencias principales
- `requirements-notebooks.txt`: Extras para notebooks y experimentación
- `.env`: Variables de entorno (no versionar)
- `Dockerfile`: Soporte para despliegue en contenedores

---

## Contribuciones

¡Las contribuciones son bienvenidas! Puedes ayudar mejorando el código, añadiendo notebooks, pruebas o reportando bugs.

1. Haz fork del repo.
2. Crea una rama:  `git checkout -b mi-nueva-rama`
3. Verifica que tu código pase las pruebas (`pytest`).
4. Haz pull request con tu descripción.

---

## FAQ

### 1. ¿Error al conectar a MongoDB?

Verifica que el URI en `.env` sea correcto.
Ejemplo:
```env
MONGO_URI=mongodb://localhost:27017/mi_base_de_datos
```

### 2. `ModuleNotFoundError` al ejecutar la API o un notebook

Instala dependencias:
```bash
pip install -r requirements.txt
pip install -r requirements-notebooks.txt  # si usas notebooks
```

---

## Licencia

MIT. Consulta `LICENSE` para más detalles.