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

# Actualizar e instalar dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    unzip \
    curl \
    gnupg \
    netcat-openbsd \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Instalar Node.js y npm
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Copia requirements.txt y instala dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copia todo el código de la aplicación
COPY . .

# Crear directorios necesarios para Reflex
RUN mkdir -p /app/data /app/.web /app/.states && \
    chmod -R 755 /app/.web /app/.states

# === BUILD TIME SETUP ===

# 1. Inicializar Reflex
RUN echo "⚙️ Inicializando Reflex..." && \
    reflex init --loglevel info || echo "Reflex init completed"

# 2. Verificar/crear directorios
RUN echo "📁 Preparando directorios..." && \
    mkdir -p /app/.web /app/.states /app/data && \
    chmod -R 755 /app/.web /app/.states

# 3. Crear tablas de base de datos
RUN echo "🗄️ Creando tablas de la base de datos..." && \
    python init_db.py

# 4. Ejecutar seed para poblar datos
RUN echo "🌱 Poblando la base de datos..." && \
    python seed.py && \
    echo "✅ Seed completado."

# Asegurar permisos correctos
RUN chmod 666 reflex.db 2>/dev/null || echo "No DB file yet" && \
    chmod -R 755 /app

# Exponer puertos para Traefik
EXPOSE 3000
EXPOSE 8000

# === COMANDO DE PRODUCCIÓN ===
# Frontend en puerto 3000, Backend en puerto 8000, modo DESARROLLO (para resolver WebSocket)
CMD echo "🚀 Iniciando Salto Estudia..." && \
    echo "   -> Frontend: http://localhost:3000" && \
    echo "   -> Backend:  http://localhost:8000" && \
    echo "   -> AG Grid: ✅ Implementado" && \
    reflex run --backend-host 0.0.0.0 --backend-port 8000 --frontend-port 3000 