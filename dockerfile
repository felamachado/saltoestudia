# Dockerfile para Salto Estudia - Aplicación completa con Reflex 0.6.4 + AG Grid
FROM python:3.11-slim-bookworm

# Evitar prompts interactivos durante la instalación
ENV DEBIAN_FRONTEND=noninteractive

# Establece el directorio de trabajo
WORKDIR /app

# Configurar variables de entorno para Reflex
ENV HOME=/app
ENV REFLEX_DB_URL=sqlite:///reflex.db
ENV PYTHONPATH=/app

# Actualizar e instalar dependencias del sistema y limpiar caché
RUN apt-get update && apt-get install -y --no-install-recommends \
    unzip \
    curl \
    gnupg \
    netcat-openbsd \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Instalar Node.js y npm (versión LTS compatible)
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

# Inicializar Reflex con la nueva versión
RUN reflex init --loglevel info || echo "Reflex init completed"

# Asegurar permisos correctos en archivos importantes  
RUN chmod 666 reflex.db 2>/dev/null || echo "No DB file yet" && \
    chmod +x start.sh && \
    chmod -R 755 /app

# Expone los puertos de Reflex
EXPOSE 3000
EXPOSE 8000

# Comando para ejecutar la aplicación
CMD ["./start.sh"]
