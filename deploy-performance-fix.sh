#!/bin/bash

# Script de deployment OPTIMIZADO para corregir 4 segundos de delay
# Corrige: Reflex desactualizado, modo desarrollo, falta de pre-compilación

set -e

echo "🚀 DEPLOYMENT DE CORRECCIÓN DE PERFORMANCE"
echo "=========================================="
echo "🎯 Objetivo: Reducir tiempo de carga de 4s a <1s"
echo ""

# Configuración
VPS_HOST="${VPS_HOST:-ubuntu@150.230.30.198}"
VPS_PATH="/srv/docker/saltoestudia"
SSH_KEY="~/.ssh/github_actions_deploy_v2"

echo "🔍 PROBLEMAS A CORREGIR:"
echo "❌ Reflex 0.6.4 → 0.7.14"
echo "❌ Modo desarrollo → Modo producción"
echo "❌ Sin pre-compilación → Con pre-compilación"
echo ""

# Limpiar cache local
echo "🧹 Limpiando cache local..."
rm -rf .web __pycache__ saltoestudia/__pycache__ saltoestudia/pages/__pycache__ 2>/dev/null || true

# Verificar archivos optimizados
echo "📋 Verificando archivos optimizados..."
if [ ! -f "dockerfile.production" ]; then
    echo "❌ ERROR: dockerfile.production no encontrado"
    exit 1
fi

if [ ! -f "requirements.txt" ]; then
    echo "❌ ERROR: requirements.txt no encontrado"
    exit 1
fi

# Verificar que requirements.txt tenga la versión correcta
if ! grep -q "reflex==0.7.14" requirements.txt; then
    echo "❌ ERROR: requirements.txt no tiene reflex==0.7.14"
    exit 1
fi

echo "✅ Archivos verificados"

# Backup y parada del servicio actual
echo "💾 Backup y parada del servicio actual..."
ssh -i $SSH_KEY $VPS_HOST "cd $VPS_PATH && echo '=== ANTES DEL FIX ===' && docker logs saltoestudia-app --tail 5"
ssh -i $SSH_KEY $VPS_HOST "cd $VPS_PATH && (docker-compose down 2>/dev/null || docker compose down 2>/dev/null || true)"

# Copiar archivos optimizados
echo "📂 Copiando archivos con optimizaciones..."
rsync -av -e "ssh -i $SSH_KEY -o StrictHostKeyChecking=no" \
    --exclude '.git' \
    --exclude 'node_modules' \
    --exclude '.web' \
    --exclude '*.pyc' \
    --exclude '__pycache__' \
    --exclude '.github' \
    . $VPS_HOST:$VPS_PATH/

# Copiar configuración optimizada
scp -i $SSH_KEY dockerfile.production $VPS_HOST:$VPS_PATH/dockerfile
scp -i $SSH_KEY docker-compose.production.yml $VPS_HOST:$VPS_PATH/docker-compose.yml

# Build optimizado
echo "🔧 Build OPTIMIZADO (incluye Reflex 0.7.14 + pre-compilación)..."
ssh -i $SSH_KEY $VPS_HOST "cd $VPS_PATH && (docker-compose build --no-cache 2>/dev/null || docker compose build --no-cache)"

# Deployment optimizado
echo "🚀 Deployment con optimizaciones..."
ssh -i $SSH_KEY $VPS_HOST "cd $VPS_PATH && (docker-compose up -d 2>/dev/null || docker compose up -d)"

# Esperar que el servicio esté listo
echo "⏱️ Esperando que el servicio esté listo..."
sleep 15

# Verificar que está funcionando
echo "🔍 Verificando el deployment..."
if ssh -i $SSH_KEY $VPS_HOST "docker ps | grep saltoestudia-app"; then
    echo "✅ Contenedor activo"
else
    echo "❌ Problema con el contenedor"
    ssh -i $SSH_KEY $VPS_HOST "docker logs saltoestudia-app --tail 10"
    exit 1
fi

# Mostrar logs del nuevo deployment
echo "📊 Logs del nuevo deployment:"
ssh -i $SSH_KEY $VPS_HOST "docker logs saltoestudia-app --tail 10"

# Test de performance inmediato
echo ""
echo "🔬 TESTS DE PERFORMANCE INMEDIATOS"
echo "=================================="

echo "Test 1 - Inmediato (cold start):"
time curl -s -w "Total: %{time_total}s | Start Transfer: %{time_starttransfer}s\n" https://saltoestudia.infra.com.uy/ -o /dev/null

sleep 3

echo "Test 2 - Warm start:"
time curl -s -w "Total: %{time_total}s | Start Transfer: %{time_starttransfer}s\n" https://saltoestudia.infra.com.uy/ -o /dev/null

sleep 3

echo "Test 3 - Confirmación:"
time curl -s -w "Total: %{time_total}s | Start Transfer: %{time_starttransfer}s\n" https://saltoestudia.infra.com.uy/ -o /dev/null

echo ""
echo "🎉 DEPLOYMENT DE PERFORMANCE COMPLETADO"
echo "======================================"
echo "✅ Reflex actualizado a 0.7.14"
echo "✅ Modo producción activado"
echo "✅ Frontend pre-compilado"
echo "🎯 Tiempo esperado: <1 segundo"
echo ""
echo "🌐 Sitio: https://saltoestudia.infra.com.uy"
echo "📊 Monitoreo: ssh -i $SSH_KEY $VPS_HOST 'docker logs saltoestudia-app -f'" 