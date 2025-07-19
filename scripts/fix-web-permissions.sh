#!/bin/bash

# Script para solucionar problemas de permisos del directorio .web en Reflex
# Uso: ./scripts/fix-web-permissions.sh

set -e

echo "🔧 Solucionando problemas de permisos del directorio .web..."

# 1. Detener todos los procesos de Reflex
echo "📋 Deteniendo procesos de Reflex..."
sudo pkill -f "reflex run" 2>/dev/null || true
pkill -f "reflex run" 2>/dev/null || true
sleep 2

# 2. Eliminar completamente el directorio .web problemático
echo "🗑️  Eliminando directorio .web problemático..."
sudo rm -rf .web 2>/dev/null || true

# 3. Corregir permisos del proyecto
echo "🔐 Corrigiendo permisos del proyecto..."
sudo chown -R $(whoami):$(whoami) .

# 4. Verificar que no existe .web
if [ -d ".web" ]; then
    echo "❌ Error: El directorio .web aún existe"
    exit 1
else
    echo "✅ Directorio .web eliminado correctamente"
fi

# 5. Verificar permisos
echo "📋 Verificando permisos..."
ls -la | grep -E "\.(py|md|txt|json)$" | head -5

echo ""
echo "🎉 ¡Problema solucionado!"
echo ""
echo "📝 Para ejecutar Reflex:"
echo "   reflex run"
echo ""
echo "📝 Para verificar que funciona:"
echo "   curl -s http://localhost:3000 | head -5"
echo ""
echo "⚠️  IMPORTANTE: NUNCA ejecutes 'sudo reflex run'"
echo "   Siempre usa 'reflex run' como usuario normal" 