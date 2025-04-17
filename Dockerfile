FROM python:3.12-slim

WORKDIR /app

# Instalar dependencias del sistema (necesarias para Twikit y transformers)
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copiar e instalar dependencias de Python PRIMERO (para caché eficiente)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar TODO el proyecto (excepto lo excluido en .dockerignore)
COPY . .

# Variables de entorno (opcional, pero recomendado usar --env-file en producción)
ENV PYTHONPATH=/app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]