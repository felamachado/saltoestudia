#!/bin/bash

# =============================================================================
# Script de Arranque Completo para Salto Estudia
# =============================================================================
# 
# Este script combina la limpieza de puertos y el arranque de Reflex
# en un solo comando para facilitar el desarrollo.
#
# Uso: ./scripts/arrancar_app.sh
#
# Compatibilidad: Linux (Ubuntu, Debian, CentOS, etc.)
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

# Obtener el directorio del script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

print_status "🚀 Iniciando arranque completo de Salto Estudia..."
echo ""

# Verificar que estamos en el directorio correcto
if [ ! -f "$PROJECT_ROOT/rxconfig.py" ]; then
    print_error "No se encontró rxconfig.py en $PROJECT_ROOT"
    print_error "Asegúrate de ejecutar este script desde la carpeta del proyecto."
    exit 1
fi

print_success "✓ Directorio del proyecto verificado: $PROJECT_ROOT"
echo ""

# Navegar al directorio del proyecto
cd "$PROJECT_ROOT"

# Ejecutar limpieza de puertos
print_status "🧹 Ejecutando limpieza de puertos..."
if [ -f "./scripts/limpiar_puertos.sh" ]; then
    ./scripts/limpiar_puertos.sh
else
    print_warning "Script de limpieza no encontrado. Continuando sin limpieza..."
fi

echo ""
print_status "🎯 Arrancando Reflex..."
echo ""

# Verificar que Reflex está instalado
if ! command -v reflex &> /dev/null; then
    print_error "Reflex no está instalado. Instalando..."
    pip install reflex
fi

# Arrancar Reflex
print_success "✅ Iniciando Reflex con configuración optimizada..."
echo ""
print_status "📱 La aplicación estará disponible en:"
echo "   - Frontend: http://localhost:3000"
echo "   - Backend:  http://localhost:8000"
echo "   - Admin:    http://localhost:3000/admin"
echo ""
print_status "🔄 Presiona Ctrl+C para detener la aplicación"
echo ""

# Ejecutar Reflex con la configuración correcta
reflex run --backend-host 0.0.0.0 --backend-port 8000 --frontend-port 3000 