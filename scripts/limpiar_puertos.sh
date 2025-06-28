#!/bin/bash

# =============================================================================
# Script de Limpieza de Puertos para Salto Estudia
# =============================================================================
# 
# Este script identifica y mata procesos que están ocupando los puertos
# utilizados por la aplicación Salto Estudia (3000 y 8000).
#
# Uso: ./scripts/limpiar_puertos.sh
#      O desde cualquier carpeta: /ruta/completa/saltoestudia/scripts/limpiar_puertos.sh
#
# Compatibilidad: Linux (Ubuntu, Debian, CentOS, etc.)
# Entornos: Local, VPS, CI/CD, Docker
# =============================================================================

set -e  # Salir si hay algún error

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para imprimir mensajes con colores
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_status "🧹 Iniciando limpieza de puertos para Salto Estudia..."
echo ""

# Puertos a verificar
PORTS=(3000 8000)
PROCESSES_FOUND=false

# Función para verificar y matar procesos en un puerto
check_and_kill_port() {
    local port=$1
    local processes=$(lsof -ti:$port 2>/dev/null)
    
    if [ -n "$processes" ]; then
        print_warning "⚠️  Puerto $port está ocupado por los siguientes procesos:"
        echo ""
        
        for pid in $processes; do
            local process_info=$(ps -p $pid -o pid,ppid,cmd --no-headers 2>/dev/null)
            if [ -n "$process_info" ]; then
                echo "   PID: $pid - $process_info"
            fi
        done
        echo ""
        
        print_status "🔄 Matando procesos en puerto $port automáticamente..."
        echo "$processes" | xargs -r kill -9
        sleep 1
        
        # Verificar si se mataron correctamente
        if lsof -ti:$port >/dev/null 2>&1; then
            print_error "❌ No se pudieron matar todos los procesos en puerto $port"
        else
            print_success "✅ Puerto $port liberado correctamente"
        fi
        echo ""
        PROCESSES_FOUND=true
    else
        print_success "✅ Puerto $port está libre"
    fi
}

# Verificar cada puerto
for port in "${PORTS[@]}"; do
    check_and_kill_port $port
done

# Resumen final
if [ "$PROCESSES_FOUND" = true ]; then
    print_success "🎉 Limpieza de puertos completada"
    echo ""
    print_status "📋 Resumen:"
    print_status "   - Puerto 3000: Libre para frontend"
    print_status "   - Puerto 8000: Libre para backend"
    echo ""
    print_status "✅ Ya puedes arrancar la aplicación con:"
    print_status "   ./scripts/arrancar_app.sh"
    echo ""
else
    print_success "🎉 Todos los puertos ya estaban libres"
    echo ""
    print_status "✅ Ya puedes arrancar la aplicación con:"
    print_status "   ./scripts/arrancar_app.sh"
    echo ""
fi 