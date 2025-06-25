#!/bin/bash
# ========================================
# SCRIPT DE DESPLIEGUE - SALTO ESTUDIA VPS ORACLE
# ========================================
# Automatiza el despliegue en /srv/docker/saltoestudia

set -e  # Salir si hay errores

VPS_HOST="ubuntu@150.230.30.198"
VPS_PATH="/srv/docker/saltoestudia"
DOMAIN="saltoestudia.infra.com.uy"

echo "🚀 DESPLEGANDO SALTO ESTUDIA EN VPS ORACLE"
echo "=========================================="
echo "VPS: $VPS_HOST"
echo "Ruta: $VPS_PATH"
echo "Dominio: $DOMAIN"
echo ""

# Verificar conexión SSH
echo "🔐 Verificando conexión SSH..."
ssh $VPS_HOST "echo 'Conexión exitosa'"

# Crear directorio en VPS si no existe
echo "📁 Preparando directorio en VPS..."
ssh $VPS_HOST "sudo mkdir -p $VPS_PATH/{data,logs}"
ssh $VPS_HOST "sudo chown -R ubuntu:ubuntu $VPS_PATH"

# Sincronizar código (excluyendo archivos innecesarios)
echo "📤 Sincronizando código..."
rsync -avz --progress \
    --exclude='.git' \
    --exclude='__pycache__' \
    --exclude='.web' \
    --exclude='.states' \
    --exclude='node_modules' \
    --exclude='.env' \
    --exclude='*.db' \
    ./ $VPS_HOST:$VPS_PATH/

# Configurar archivo de entorno de producción
echo "⚙️ Configurando variables de entorno..."
ssh $VPS_HOST "cd $VPS_PATH && cp env.production.example .env"

# Construir y ejecutar
echo "🐳 Construyendo y ejecutando contenedor..."
ssh $VPS_HOST "cd $VPS_PATH && docker-compose -f docker-compose.production.yml down || true"
ssh $VPS_HOST "cd $VPS_PATH && docker-compose -f docker-compose.production.yml build"
ssh $VPS_HOST "cd $VPS_PATH && docker-compose -f docker-compose.production.yml up -d"

# Verificar estado
echo "✅ Verificando despliegue..."
sleep 10
ssh $VPS_HOST "docker ps | grep saltoestudia"

echo ""
echo "🎉 ¡DESPLIEGUE COMPLETADO!"
echo "=========================================="
echo "🌐 URL: https://$DOMAIN"
echo "📊 Logs: ssh $VPS_HOST 'docker logs -f saltoestudia-app'"
echo "🔧 Gestión: ssh $VPS_HOST 'cd $VPS_PATH'"
echo "" 