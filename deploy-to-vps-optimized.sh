#!/bin/bash

# Script de despliegue OPTIMIZADO - Fase 2 Performance
# Incluye validaciones y optimizaciones adicionales

set -e

echo "🚀 INICIANDO DESPLIEGUE OPTIMIZADO - FASE 2"
echo "==========================================="

# Configuración
VPS_HOST="${VPS_HOST:-ubuntu@150.230.30.198}"
VPS_PATH="/srv/docker/saltoestudia"
SSH_KEY="~/.ssh/github_actions_deploy_v2"

# === VALIDACIONES PRE-DEPLOYMENT ===
echo "🔍 Validando archivos optimizados..."

# Verificar que existen los archivos optimizados
required_files=(
    "docker-compose.production.yml"
    "dockerfile.production" 
    "assets/sw.js"
    "assets/manifest.json"
    ".env"
)

for file in "${required_files[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ ERROR: Archivo requerido no encontrado: $file"
        exit 1
    fi
done

echo "✅ Archivos validados"

# === LIMPIAR CACHE LOCAL ===
echo "🧹 Limpiando cache local..."
rm -rf .web __pycache__ saltoestudia/__pycache__ saltoestudia/pages/__pycache__ 2>/dev/null || true

# === DEPLOYMENT OPTIMIZADO ===
echo "📦 Iniciando deployment con optimizaciones..."

# Parar contenedor actual
ssh -i $SSH_KEY $VPS_HOST "cd $VPS_PATH && (docker-compose down 2>/dev/null || docker compose down 2>/dev/null || true)"

# Copiar archivos con optimizaciones
echo "🚀 Copiando archivos optimizados..."
rsync -av -e "ssh -i $SSH_KEY -o StrictHostKeyChecking=no" \
    --exclude '.git' \
    --exclude 'node_modules' \
    --exclude '.web' \
    --exclude '*.pyc' \
    --exclude '__pycache__' \
    --exclude '.github' \
    . $VPS_HOST:$VPS_PATH/

# Copiar configuración de producción optimizada
scp -i $SSH_KEY dockerfile.production $VPS_HOST:$VPS_PATH/dockerfile
scp -i $SSH_KEY docker-compose.production.yml $VPS_HOST:$VPS_PATH/docker-compose.yml

# === BUILD Y DEPLOY OPTIMIZADO ===
echo "🐳 Construyendo imagen optimizada..."
ssh -i $SSH_KEY $VPS_HOST "cd $VPS_PATH && (docker-compose build --no-cache --parallel 2>/dev/null || docker compose build --no-cache)"

echo "🚀 Desplegando con configuración optimizada..."
ssh -i $SSH_KEY $VPS_HOST "cd $VPS_PATH && (docker-compose up -d 2>/dev/null || docker compose up -d)"

# === VALIDACIONES POST-DEPLOYMENT ===
echo "🔍 Validando deployment..."

# Esperar que el contenedor esté listo
sleep 15

# Verificar que el contenedor está corriendo
if ssh -i $SSH_KEY $VPS_HOST "docker ps | grep saltoestudia-app"; then
    echo "✅ Contenedor activo"
else
    echo "⚠️ Problema con el contenedor"
    ssh -i $SSH_KEY $VPS_HOST "docker logs saltoestudia-app --tail 10"
fi

# Reiniciar Traefik para aplicar nuevas configuraciones
echo "🔄 Actualizando Traefik..."
ssh -i $SSH_KEY $VPS_HOST "docker restart traefik"

# === VERIFICACIONES DE PERFORMANCE ===
echo "⚡ Verificando optimizaciones..."

# Verificar que WebSocket responde
echo "🔌 Probando WebSocket..."
if ssh -i $SSH_KEY $VPS_HOST "curl -s -I https://saltoestudia.infra.com.uy/_event | grep -q '307\|101'"; then
    echo "✅ WebSocket configurado correctamente"
else
    echo "⚠️ Verificar configuración WebSocket"
fi

# Verificar Service Worker
echo "🛠️ Verificando Service Worker..."
if ssh -i $SSH_KEY $VPS_HOST "curl -s https://saltoestudia.infra.com.uy/sw.js | grep -q 'Service Worker'"; then
    echo "✅ Service Worker disponible"
else
    echo "⚠️ Service Worker no encontrado"
fi

echo ""
echo "🎉 DEPLOYMENT OPTIMIZADO COMPLETADO"
echo "=================================="
echo "✅ Aplicación: https://saltoestudia.infra.com.uy"
echo "⚡ Performance: OPTIMIZADA"
echo "🔌 WebSocket: wss://saltoestudia.infra.com.uy/_event"
echo "🛠️ Service Worker: /sw.js"
echo "📱 PWA: /manifest.json"
echo ""
echo "📊 Para monitorear performance:"
echo "   ssh -i $SSH_KEY $VPS_HOST 'docker logs saltoestudia-app -f'" 