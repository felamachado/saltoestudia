#!/bin/bash

# =============================================================================
# Script de Limpieza de Puertos para Salto Estudia
# =============================================================================
# 
# Este script mata cualquier proceso que esté ocupando los puertos 8000 y 3000,
# que son utilizados por Reflex para el backend y frontend respectivamente.
#
# Uso: ./scripts/limpiar_puertos.sh
#
# Compatibilidad: Linux (Ubuntu, Debian, CentOS, etc.)
# Requisitos: lsof (normalmente instalado por defecto)
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

# Verificar si lsof está instalado
if ! command -v lsof &> /dev/null; then
    print_error "lsof no está instalado. Instalando..."
    if command -v apt-get &> /dev/null; then
        sudo apt-get update && sudo apt-get install -y lsof
    elif command -v yum &> /dev/null; then
        sudo yum install -y lsof
    elif command -v dnf &> /dev/null; then
        sudo dnf install -y lsof
    else
        print_error "No se pudo instalar lsof automáticamente. Por favor instálalo manualmente."
        exit 1
    fi
fi

print_status "Iniciando limpieza de puertos para Salto Estudia..."
echo ""

# Puertos a limpiar
PUERTOS=(8000 3000)

for puerto in "${PUERTOS[@]}"; do
    print_status "Verificando puerto $puerto..."
    
    # Buscar procesos usando el puerto
    pids=$(lsof -ti tcp:$puerto 2>/dev/null || true)
    
    if [ -z "$pids" ]; then
        print_success "Puerto $puerto está libre."
    else
        print_warning "Encontrados procesos en puerto $puerto:"
        
        # Mostrar información de los procesos
        for pid in $pids; do
            if [ -n "$pid" ]; then
                proceso_info=$(ps -p $pid -o pid,ppid,cmd --no-headers 2>/dev/null || echo "Proceso $pid")
                echo "  - PID: $pid | $proceso_info"
            fi
        done
        
        # Preguntar si matar los procesos
        echo ""
        read -p "¿Deseas matar estos procesos? (y/N): " -n 1 -r
        echo ""
        
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            for pid in $pids; do
                if [ -n "$pid" ]; then
                    print_status "Matando proceso $pid..."
                    if kill -9 $pid 2>/dev/null; then
                        print_success "Proceso $pid terminado exitosamente."
                    else
                        print_warning "No se pudo terminar el proceso $pid (puede que ya no exista)."
                    fi
                fi
            done
        else
            print_warning "Procesos en puerto $puerto no fueron terminados."
        fi
    fi
    
    echo ""
done

# Verificación final
print_status "Verificación final de puertos..."
echo ""

for puerto in "${PUERTOS[@]}"; do
    pids=$(lsof -ti tcp:$puerto 2>/dev/null || true)
    if [ -z "$pids" ]; then
        print_success "✓ Puerto $puerto está libre y listo para usar."
    else
        print_warning "⚠ Puerto $puerto aún tiene procesos activos."
    fi
done

echo ""
print_success "Limpieza completada. Ahora puedes arrancar Reflex sin problemas."
echo ""
print_status "Próximos pasos:"
echo "1. Navega a la carpeta raíz del proyecto: cd ~/Escritorio/Proyectos/saltoestudia"
echo "2. Arranca Reflex: reflex run --backend-host 0.0.0.0 --backend-port 8000 --frontend-port 3000"
echo "" 