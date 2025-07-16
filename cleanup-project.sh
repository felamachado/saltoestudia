#!/bin/bash

# =============================================================================
# Script de Limpieza del Proyecto - Salto Estudia
# =============================================================================
# 
# Este script elimina archivos innecesarios, temporales y de desarrollo
# que no son necesarios para el funcionamiento del proyecto.
#
# Uso: ./cleanup-project.sh
# =============================================================================

set -e

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

echo "🧹 LIMPIEZA DEL PROYECTO SALTO ESTUDIA"
echo "======================================"
echo ""

# Función para verificar si un archivo existe antes de eliminarlo
safe_remove() {
    if [ -e "$1" ]; then
        rm -rf "$1"
        print_success "✅ Eliminado: $1"
    else
        print_status "ℹ️ No existe: $1"
    fi
}

# 1. Limpiar archivos de cache de Python
print_status "1. Limpiando cache de Python..."
safe_remove "__pycache__"
safe_remove "saltoestudia/__pycache__"
safe_remove "saltoestudia/pages/__pycache__"
safe_remove "scripts/__pycache__"
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true
find . -name "*.pyo" -delete 2>/dev/null || true

# 2. Limpiar cache de Reflex
print_status "2. Limpiando cache de Reflex..."
safe_remove ".web"
safe_remove ".states"

# 3. Limpiar archivos de logs temporales
print_status "3. Limpiando archivos de logs temporales..."
safe_remove "reflex.log"
safe_remove "wget-log"
safe_remove "*.log"

# 4. Limpiar archivos de base de datos temporales
print_status "4. Limpiando archivos de base de datos temporales..."
safe_remove "reflex.db"

# 5. Limpiar archivos de desarrollo duplicados
print_status "5. Limpiando archivos de desarrollo duplicados..."
safe_remove "deploy-performance-fix.sh"
safe_remove "deploy-to-vps-optimized.sh"

# 6. Limpiar directorios de node_modules innecesarios
print_status "6. Limpiando node_modules innecesarios..."
if [ -d "node_modules" ] && [ ! -f "package.json" ]; then
    safe_remove "node_modules"
fi

# 7. Limpiar archivos temporales del sistema
print_status "7. Limpiando archivos temporales del sistema..."
find . -name ".DS_Store" -delete 2>/dev/null || true
find . -name "Thumbs.db" -delete 2>/dev/null || true
find . -name "*.tmp" -delete 2>/dev/null || true
find . -name "*.temp" -delete 2>/dev/null || true

# 8. Limpiar archivos de IDE
print_status "8. Limpiando archivos de IDE..."
safe_remove ".vscode"
safe_remove ".idea"
safe_remove "*.swp"
safe_remove "*.swo"
safe_remove "*~"

# 9. Verificar archivos importantes que NO se deben eliminar
print_status "9. Verificando archivos importantes..."
IMPORTANT_FILES=(
    "docker-compose.yml"
    "docker-compose.production.yml"
    "dockerfile"
    "dockerfile.production"
    "deploy-to-vps.sh"
    "requirements.txt"
    "rxconfig.py"
    "saltoestudia/saltoestudia.py"
    "data/saltoestudia.db"
    ".env"
)

for file in "${IMPORTANT_FILES[@]}"; do
    if [ -e "$file" ]; then
        print_success "✅ Importante: $file (conservado)"
    else
        print_warning "⚠️ Importante faltante: $file"
    fi
done

# 10. Mostrar estadísticas de limpieza
print_status "10. Estadísticas de limpieza..."
echo "📊 Espacio liberado:"
du -sh . 2>/dev/null | head -1

echo ""
echo "🎉 LIMPIEZA COMPLETADA"
echo "====================="
print_success "✅ Proyecto limpiado exitosamente"
echo ""
print_status "📋 Archivos eliminados:"
print_status "   - Cache de Python (__pycache__, *.pyc)"
print_status "   - Cache de Reflex (.web, .states)"
print_status "   - Logs temporales (*.log, wget-log)"
print_status "   - Archivos de desarrollo duplicados"
print_status "   - Archivos temporales del sistema"
print_status "   - Archivos de IDE (.vscode, .idea)"
echo ""
print_status "💡 Para reconstruir el cache:"
print_status "   ./scripts/start-project.sh docker"
echo "" 