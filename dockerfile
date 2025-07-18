# Dockerfile para PRODUCCIÓN - Salto Estudia VPS
# Optimizado para Traefik con frontend/backend separados
FROM python:3.11-slim-bookworm

# Evitar prompts interactivos durante la instalación
ENV DEBIAN_FRONTEND=noninteractive

# Establece el directorio de trabajo
WORKDIR /app

# Configurar variables de entorno para Reflex
ENV HOME=/app
ENV REFLEX_DB_URL=sqlite:///reflex.db
ENV PYTHONPATH=/app

# Variables de entorno para la base de datos
ENV DATABASE_URL=sqlite:///./data/saltoestudia.db

# Instalar Node.js y unzip
RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copiar archivos del proyecto
COPY . .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Instalar dependencias de Node.js
RUN npm install --legacy-peer-deps

# Exponer puertos
EXPOSE 3000 8000

# Comando por defecto (puede ser sobrescrito en docker-compose)
CMD ["reflex", "run"] 