#!/bin/bash

# Script para ejecutar Reflex limpiando puertos automáticamente
# Uso: ./scripts/reflex-clean.sh

echo "🧹 Limpiando puertos antes de ejecutar Reflex..."

# Función para liberar un puerto
liberar_puerto() {
    local puerto=$1
    echo "   Liberando puerto $puerto..."
    
    # Intentar con fuser primero (más limpio)
    if command -v fuser &> /dev/null; then
        fuser -k $puerto/tcp 2>/dev/null || true
    else
        # Fallback con lsof
        lsof -ti:$puerto 2>/dev/null | xargs kill -9 2>/dev/null || true
    fi
    
    # Esperar un momento para que se libere
    sleep 1
}

# Liberar puertos
liberar_puerto 3000
liberar_puerto 8000

echo "✅ Puertos liberados. Iniciando Reflex..."
echo ""

# Ejecutar Reflex
reflex run 