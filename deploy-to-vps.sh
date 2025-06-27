#!/bin/bash

# Script de despliegue automatizado para Salto Estudia
# Despliega al VPS Oracle Cloud con Traefik
# Versión GitHub Actions - Usa clave SSH específica

set -e  # Salir si hay errores

# Configuración
VPS_HOST="${VPS_HOST:-ubuntu@150.230.30.198}"
VPS_HOST_IP="${VPS_HOST_IP:-150.230.30.198}"
VPS_PATH="/srv/docker/saltoestudia"
LOCAL_ENV=".env"
LOCAL_DATA="data"

# Detectar si estamos en GitHub Actions
if [ -n "$GITHUB_ACTIONS" ]; then
    SSH_KEY="~/.ssh/github_actions_deploy_v2"
    echo "🤖 Ejecutando desde GitHub Actions"
else
    SSH_KEY="~/.ssh/github_actions_deploy_v2"
    echo "💻 Ejecutando localmente"
fi

echo "🚀 INICIANDO DESPLIEGUE DE SALTO ESTUDIA"
echo "========================================"
echo "🔑 Usando clave SSH: $SSH_KEY"
echo "🖥️  Destino: $VPS_HOST"
echo ""

# Verificar archivos necesarios
echo "📋 Verificando archivos locales..."
if [ ! -f "$LOCAL_ENV" ]; then
    echo "❌ ERROR: No se encuentra .env"
    exit 1
fi

if [ ! -d "$LOCAL_DATA" ]; then
    echo "❌ ERROR: No se encuentra carpeta data/"
    exit 1
fi

if [ ! -f "dockerfile.production" ]; then
    echo "❌ ERROR: No se encuentra dockerfile.production"
    exit 1
fi

if [ ! -f "docker-compose.production.yml" ]; then
    echo "❌ ERROR: No se encuentra docker-compose.production.yml"
    exit 1
fi

echo "✅ Archivos locales verificados"

# Crear directorio en VPS si no existe
echo "📁 Preparando directorio en VPS..."
ssh -i $SSH_KEY -o StrictHostKeyChecking=no $VPS_HOST "mkdir -p $VPS_PATH"

# Verificar dependencias en VPS
echo "🔧 Verificando dependencias en VPS..."
ssh -i $SSH_KEY $VPS_HOST "command -v rsync >/dev/null 2>&1 || (echo '📦 Instalando rsync...' && sudo apt-get update -qq && sudo apt-get install -y rsync)"
ssh -i $SSH_KEY $VPS_HOST "command -v docker-compose >/dev/null 2>&1 && echo '✓ docker-compose disponible' || echo '⚠️ Usando docker compose en lugar de docker-compose'"

# Detectar si usar docker-compose o docker compose
DOCKER_COMPOSE_CMD="docker compose"
ssh -i $SSH_KEY $VPS_HOST "command -v docker-compose >/dev/null 2>&1" && DOCKER_COMPOSE_CMD="docker-compose"
echo "🐳 Usando comando: $DOCKER_COMPOSE_CMD"

# Backup de la configuración actual (si existe)
echo "💾 Haciendo backup de configuración actual..."
ssh -i $SSH_KEY $VPS_HOST "cd $VPS_PATH && (docker-compose down 2>/dev/null || docker compose down 2>/dev/null || true)"
ssh -i $SSH_KEY $VPS_HOST "cd $VPS_PATH && [ -f docker-compose.yml ] && cp docker-compose.yml docker-compose.yml.backup.\$(date +%Y%m%d_%H%M%S) || true"

# Copiar archivos de código
echo "📂 Copiando código fuente..."
rsync -av -e "ssh -i $SSH_KEY -o StrictHostKeyChecking=no" --exclude '.git' --exclude 'node_modules' --exclude '.web' --exclude '*.pyc' --exclude '.github' . $VPS_HOST:$VPS_PATH/

# Copiar archivos de producción específicos
echo "⚙️ Copiando configuración de producción..."
scp -i $SSH_KEY dockerfile.production $VPS_HOST:$VPS_PATH/dockerfile
scp -i $SSH_KEY docker-compose.production.yml $VPS_HOST:$VPS_PATH/docker-compose.yml

# Copiar archivos sensibles
echo "🔐 Copiando archivos de configuración..."
scp -i $SSH_KEY $LOCAL_ENV $VPS_HOST:$VPS_PATH/
rsync -av -e "ssh -i $SSH_KEY" $LOCAL_DATA/ $VPS_HOST:$VPS_PATH/data/

# Construir y ejecutar en VPS
echo "🐳 Construyendo y desplegando en VPS..."
ssh -i $SSH_KEY $VPS_HOST "cd $VPS_PATH && (docker-compose down 2>/dev/null || docker compose down 2>/dev/null || true)"
ssh -i $SSH_KEY $VPS_HOST "cd $VPS_PATH && (docker-compose build --no-cache 2>/dev/null || docker compose build --no-cache)"
ssh -i $SSH_KEY $VPS_HOST "cd $VPS_PATH && (docker-compose up -d 2>/dev/null || docker compose up -d)"

# Reiniciar Traefik para detectar cambios
echo "🔄 Reiniciando Traefik..."
ssh -i $SSH_KEY $VPS_HOST "docker restart traefik"

# Verificar que la aplicación está corriendo
echo "🔍 Verificando deployment..."
sleep 10
ssh -i $SSH_KEY $VPS_HOST "docker ps | grep saltoestudia" && echo "✅ Contenedor activo" || echo "⚠️ Verificar contenedor"

# Mostrar status de contenedores
echo "📊 Estado de contenedores:"
ssh -i $SSH_KEY $VPS_HOST "cd $VPS_PATH && (docker-compose ps 2>/dev/null || docker compose ps 2>/dev/null || echo 'No se pudo obtener status')"

echo ""
echo "🎉 DESPLIEGUE COMPLETADO"
echo "======================="
echo "✅ Aplicación disponible en: https://saltoestudia.infra.com.uy"
echo ""
echo "📊 Para ver logs:"
echo "   ssh -i $SSH_KEY $VPS_HOST 'docker logs saltoestudia-app -f'"
echo ""
echo "🔧 Para conectarse al VPS:"
echo "   ssh -i $SSH_KEY $VPS_HOST"
echo ""
echo "🔄 Para ver estado:"
echo "   ssh -i $SSH_KEY $VPS_HOST 'cd $VPS_PATH && (docker-compose ps || docker compose ps)'" 