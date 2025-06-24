#!/bin/bash
# Script para ejecutar Salto Estudia en modo desarrollo (con hot-reload)
# Reemplaza: docker-compose up

echo "🚀 SALTO ESTUDIA - MODO DESARROLLO"
echo "=================================="
echo "Hot-reload: ✅ Activo"
echo "Frontend: http://localhost:3000"
echo "Backend: http://localhost:8000"
echo ""

# Detener contenedor anterior si existe
docker stop saltoestudia-app 2>/dev/null || true
docker rm saltoestudia-app 2>/dev/null || true

# Construir imagen
echo "📦 Construyendo imagen..."
docker build -t saltoestudia .

# Ejecutar con hot-reload (montando volúmenes)
echo "🔄 Iniciando con hot-reload..."
docker run -d \
  --name saltoestudia-app \
  -p 3000:3000 \
  -p 8000:8000 \
  -v "$(pwd)":/app \
  -v "$(pwd)/data":/app/data \
  --env-file .env 2>/dev/null || docker run -d \
  --name saltoestudia-app \
  -p 3000:3000 \
  -p 8000:8000 \
  -v "$(pwd)":/app \
  -v "$(pwd)/data":/app/data \
  saltoestudia

echo "✅ Salto Estudia ejecutándose en modo desarrollo"
echo "Puedes editar el código y los cambios se aplicarán automáticamente"
echo ""
echo "Para ver logs: docker logs -f saltoestudia-app"
echo "Para detener: docker stop saltoestudia-app" 