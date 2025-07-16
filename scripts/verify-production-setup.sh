#!/bin/bash

# Script para verificar la configuración de producción antes del deploy
# Simula las condiciones del VPS para detectar problemas temprano

set -e

echo "🔍 VERIFICACIÓN DE CONFIGURACIÓN DE PRODUCCIÓN"
echo "=============================================="

# Verificar que estamos en modo producción
echo "1. Verificando configuración de entorno..."

if [ ! -f "docker-compose.yml" ]; then
    echo "❌ Error: docker-compose.yml no encontrado"
    exit 1
fi

if [ ! -f ".env" ]; then
    echo "❌ Error: .env no encontrado"
    exit 1
fi

echo "✅ Archivos de configuración encontrados"

# Verificar configuración de docker-compose.yml
echo ""
echo "2. Verificando docker-compose.yml..."

# Verificar nombre del contenedor
if grep -q "container_name: saltoestudia-app" docker-compose.yml; then
    echo "✅ Nombre del contenedor correcto: saltoestudia-app"
else
    echo "❌ Error: Nombre del contenedor incorrecto (debe ser saltoestudia-app)"
    exit 1
fi

# Verificar dominio de producción
if grep -q "saltoestudia.infra.com.uy" docker-compose.yml; then
    echo "✅ Dominio de producción correcto: saltoestudia.infra.com.uy"
else
    echo "❌ Error: Dominio incorrecto (debe ser saltoestudia.infra.com.uy)"
    exit 1
fi

# Verificar que NO hay configuración de desarrollo
if grep -q "desarrollo.saltoestudia.infra.com.uy" docker-compose.yml; then
    echo "❌ Error: Configuración de desarrollo encontrada en docker-compose.yml"
    exit 1
fi

if grep -q "saltoestudia-dev" docker-compose.yml; then
    echo "❌ Error: Nombres de desarrollo encontrados en docker-compose.yml"
    exit 1
fi

echo "✅ Configuración de Traefik correcta"

# Verificar variables de entorno
echo ""
echo "3. Verificando variables de entorno..."

# Verificar que no hay contraseñas de desarrollo
if grep -q "dev_password_123" .env; then
    echo "❌ Error: Contraseñas de desarrollo encontradas en .env"
    echo "   Ejecuta: ./scripts/setup-env.sh produccion"
    exit 1
fi

# Verificar que hay contraseñas configuradas
if grep -q "CHANGE_THIS_PASSWORD_NOW" .env; then
    echo "⚠️  Advertencia: Contraseñas por defecto encontradas"
    echo "   Configura contraseñas seguras antes del deploy"
else
    echo "✅ Contraseñas configuradas"
fi

# Verificar configuración de Reflex
if grep -q "REFLEX_ENV=production" .env; then
    echo "✅ Entorno de Reflex configurado para producción"
else
    echo "⚠️  Advertencia: REFLEX_ENV no configurado para producción"
fi

# Verificar archivos necesarios
echo ""
echo "4. Verificando archivos necesarios..."

REQUIRED_FILES=(
    "dockerfile.production"
    "docker-compose.yml"
    "requirements.txt"
    "package.json"
    "saltoestudia/saltoestudia.py"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file encontrado"
    else
        echo "❌ Error: $file no encontrado"
        exit 1
    fi
done

# Verificar que la aplicación se puede construir
echo ""
echo "5. Verificando que la aplicación se puede construir..."

if command -v docker &> /dev/null; then
    echo "🔧 Intentando construir la imagen..."
    if docker build -f dockerfile.production -t saltoestudia-test . > /dev/null 2>&1; then
        echo "✅ Imagen construida exitosamente"
        docker rmi saltoestudia-test > /dev/null 2>&1 || true
    else
        echo "❌ Error: No se pudo construir la imagen"
        echo "   Ejecuta: docker build -f dockerfile.production -t saltoestudia-test ."
        exit 1
    fi
else
    echo "⚠️  Docker no disponible, saltando verificación de build"
fi

# Verificar configuración de docker-compose
echo ""
echo "6. Verificando configuración de docker-compose..."

if command -v docker-compose &> /dev/null || command -v docker &> /dev/null; then
    echo "🔧 Verificando sintaxis de docker-compose.yml..."
    if docker compose config > /dev/null 2>&1; then
        echo "✅ docker-compose.yml es válido"
    else
        echo "❌ Error: docker-compose.yml tiene errores de sintaxis"
        docker compose config
        exit 1
    fi
else
    echo "⚠️  Docker Compose no disponible, saltando verificación"
fi

echo ""
echo "🎯 VERIFICACIÓN COMPLETADA"
echo "=========================="
echo "✅ Configuración de producción lista para deploy"
echo ""
echo "📋 Resumen:"
echo "   - Contenedor: saltoestudia-app"
echo "   - Dominio: saltoestudia.infra.com.uy"
echo "   - Red: traefik-net"
echo "   - Archivos: Todos presentes"
echo ""
echo "🚀 La aplicación está lista para deploy en producción" 