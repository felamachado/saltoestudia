#!/bin/bash

# ================================================================================
# SCRIPT DE RESET COMPLETO - SALTO ESTUDIA
# ================================================================================
#
# Este script hace un reset completo del proyecto para casos extremos
# donde todo lo demás ha fallado.
#
# ⚠️  ADVERTENCIA: Este script elimina TODOS los datos del proyecto
# ⚠️  Solo usar como último recurso
#
# USO:
#   ./scripts/reset-project.sh
# ================================================================================

echo "⚠️  RESET COMPLETO DE SALTO ESTUDIA"
echo "===================================="
echo ""
echo "⚠️  ADVERTENCIA: Este script eliminará TODOS los datos del proyecto"
echo "⚠️  Incluyendo la base de datos y cualquier configuración personalizada"
echo ""

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Confirmación del usuario
echo -e "${RED}¿Estás seguro de que quieres hacer un reset completo?${NC}"
echo "Esto eliminará:"
echo "  - Base de datos SQLite"
echo "  - Contenedores Docker"
echo "  - Imágenes Docker del proyecto"
echo "  - Volúmenes de datos"
echo ""
read -p "Escribe 'RESET' para confirmar: " confirmation

if [ "$confirmation" != "RESET" ]; then
    echo "Reset cancelado."
    exit 0
fi

echo ""
echo "🔄 Iniciando reset completo..."

# ================================================================================
# PASO 1: DETENER Y ELIMINAR CONTENEDORES
# ================================================================================

print_warning "Deteniendo y eliminando contenedores..."
docker compose -f docker-compose.desarrollo.yml down --volumes --remove-orphans 2>/dev/null || true
docker compose -f docker-compose.yml down --volumes --remove-orphans 2>/dev/null || true

# ================================================================================
# PASO 2: ELIMINAR IMÁGENES DOCKER DEL PROYECTO
# ================================================================================

print_warning "Eliminando imágenes Docker del proyecto..."
docker images | grep saltoestudia | awk '{print $3}' | xargs -r docker rmi -f 2>/dev/null || true

# ================================================================================
# PASO 3: ELIMINAR VOLÚMENES Y DATOS
# ================================================================================

print_warning "Eliminando datos del proyecto..."
sudo rm -rf data/ 2>/dev/null || true
sudo rm -rf logs/ 2>/dev/null || true

# ================================================================================
# PASO 4: LIMPIAR CACHE DE DOCKER
# ================================================================================

print_warning "Limpiando cache de Docker..."
docker system prune -f 2>/dev/null || true

# ================================================================================
# PASO 5: RECREAR ESTRUCTURA BÁSICA
# ================================================================================

print_warning "Recreando estructura básica..."
mkdir -p data/
mkdir -p logs/
sudo chown -R root:root data/ 2>/dev/null || true
sudo chmod -R 777 data/ 2>/dev/null || true

# ================================================================================
# PASO 6: INICIAR PROYECTO DESDE CERO
# ================================================================================

print_warning "Iniciando proyecto desde cero..."
./scripts/start-project.sh

# ================================================================================
# RESULTADO FINAL
# ================================================================================

echo ""
echo "🎉 ¡RESET COMPLETO FINALIZADO!"
echo "==============================="
echo ""
echo "✅ Contenedores eliminados"
echo "✅ Imágenes Docker eliminadas"
echo "✅ Datos eliminados"
echo "✅ Estructura recreada"
echo "✅ Proyecto reiniciado desde cero"
echo ""
echo "🌐 Acceso a la aplicación:"
echo "   Frontend: http://localhost:3000"
echo "   Backend: http://localhost:8000"
echo ""
print_success "¡El proyecto ha sido completamente reseteado y está listo para usar!" 