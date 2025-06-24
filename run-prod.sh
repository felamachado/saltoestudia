#!/bin/bash
# Script para ejecutar Salto Estudia en modo producción (sin hot-reload)

echo "🚀 SALTO ESTUDIA - MODO PRODUCCIÓN"
echo "==================================="
echo "Hot-reload: ❌ Deshabilitado"
echo "Frontend: http://localhost:3000"
echo "Backend: http://localhost:8000"
echo ""

# Detener contenedor anterior si existe
docker stop saltoestudia-app 2>/dev/null || true
docker rm saltoestudia-app 2>/dev/null || true

# Construir imagen
echo "📦 Construyendo imagen..."
docker build -t saltoestudia:prod .

# Ejecutar sin volúmenes montados (código estático dentro del contenedor)
echo "⚡ Iniciando en modo producción..."
docker run -d \
  --name saltoestudia-app \
  -p 3000:3000 \
  -p 8000:8000 \
  --restart unless-stopped \
  --env-file .env 2>/dev/null || docker run -d \
  --name saltoestudia-app \
  -p 3000:3000 \
  -p 8000:8000 \
  --restart unless-stopped \
  saltoestudia:prod

echo "✅ Salto Estudia ejecutándose en modo producción"
echo "Código optimizado y contenido en el contenedor"
echo ""
echo "Para ver logs: docker logs -f saltoestudia-app"
echo "Para detener: docker stop saltoestudia-app" 