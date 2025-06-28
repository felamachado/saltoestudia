#!/bin/bash

# =============================================================================
# Script Global de Arranque para Salto Estudia
# =============================================================================
# 
# Este script permite arrancar la aplicación desde cualquier carpeta
# sin necesidad de navegar al directorio del proyecto.
#
# Uso: ./start.sh (desde cualquier carpeta)
#      O: /ruta/completa/saltoestudia/start.sh
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

print_status "🚀 Script Global de Arranque - Salto Estudia"
echo ""

# Obtener el directorio donde está este script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Verificar que el script está en la carpeta correcta
if [ ! -f "$SCRIPT_DIR/rxconfig.py" ]; then
    print_error "❌ Este script debe estar en la carpeta raíz del proyecto Salto Estudia"
    print_error "❌ Directorio actual: $SCRIPT_DIR"
    echo ""
    print_status "💡 Solución:"
    print_status "   Mueve este script a la carpeta raíz del proyecto:"
    print_status "   mv start.sh ~/Escritorio/Proyectos/saltoestudia/"
    echo ""
    exit 1
fi

print_success "✅ Ubicación del script verificada: $SCRIPT_DIR"
echo ""

# Ejecutar el script de arranque completo
if [ -f "$SCRIPT_DIR/scripts/arrancar_app.sh" ]; then
    print_status "🎯 Ejecutando script de arranque completo..."
    echo ""
    "$SCRIPT_DIR/scripts/arrancar_app.sh"
else
    print_error "❌ No se encontró el script de arranque en $SCRIPT_DIR/scripts/arrancar_app.sh"
    echo ""
    print_status "💡 Solución:"
    print_status "   Asegúrate de que el proyecto esté completo con todos los scripts"
    echo ""
    exit 1
fi 