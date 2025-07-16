#!/bin/bash

# ================================================================================
# SCRIPT DE DIAGNÓSTICO - SALTO ESTUDIA
# ================================================================================
#
# Este script diagnostica problemas comunes en el proyecto Salto Estudia
# y proporciona soluciones específicas para cada problema.
#
# USO:
#   ./scripts/diagnose-problems.sh
# ================================================================================

echo "🔍 Diagnóstico de Salto Estudia"
echo "================================"

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[OK]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_solution() {
    echo -e "${BLUE}[SOLUCIÓN]${NC} $1"
}

# ================================================================================
# VERIFICACIONES
# ================================================================================

echo ""
echo "1. Verificando Docker..."
if command -v docker &> /dev/null; then
    print_success "Docker está instalado"
else
    print_error "Docker no está instalado"
    print_solution "Instala Docker: https://docs.docker.com/get-docker/"
    exit 1
fi

if docker info &> /dev/null; then
    print_success "Docker está ejecutándose"
else
    print_error "Docker no está ejecutándose"
    print_solution "Inicia Docker Desktop o el servicio de Docker"
    exit 1
fi

echo ""
echo "2. Verificando contenedor..."
if docker compose -f docker-compose.desarrollo.yml ps | grep -q "Up"; then
    print_success "Contenedor está corriendo"
else
    print_error "Contenedor no está corriendo"
    print_solution "Ejecuta: ./scripts/start-project.sh"
    exit 1
fi

echo ""
echo "3. Verificando permisos de data/..."
if [ -d "data" ]; then
    PERMS=$(ls -ld data/ | awk '{print $3":"$4}')
    if [ "$PERMS" = "root:root" ]; then
        print_success "Permisos de data/ correctos"
    else
        print_warning "Permisos de data/ incorrectos: $PERMS"
        print_solution "Ejecuta: sudo chown -R root:root data/ && sudo chmod -R 777 data/"
    fi
else
    print_error "Carpeta data/ no existe"
    print_solution "Ejecuta: mkdir -p data && sudo chown -R root:root data/ && sudo chmod -R 777 data/"
fi

echo ""
echo "4. Verificando base de datos..."
DB_CHECK=$(docker compose -f docker-compose.desarrollo.yml exec -T saltoestudia-dev python -c "
from saltoestudia.database import obtener_cursos, obtener_instituciones
try:
    cursos = obtener_cursos()
    instituciones = obtener_instituciones()
    print(f'OK:{len(cursos)}:{len(instituciones)}')
except Exception as e:
    print(f'ERROR:{str(e)}')
" 2>/dev/null || echo "ERROR:No se pudo conectar")

if [[ $DB_CHECK == OK* ]]; then
    IFS=':' read -r status cursos instituciones <<< "$DB_CHECK"
    if [ "$cursos" -gt 0 ] && [ "$instituciones" -gt 0 ]; then
        print_success "Base de datos OK: $cursos cursos, $instituciones instituciones"
    else
        print_warning "Base de datos vacía: $cursos cursos, $instituciones instituciones"
        print_solution "Ejecuta: docker compose -f docker-compose.desarrollo.yml exec saltoestudia-dev python seed.py"
    fi
else
    print_error "Error en base de datos: $DB_CHECK"
    print_solution "Ejecuta: ./scripts/start-project.sh"
fi

echo ""
echo "5. Verificando aplicación web..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:3000 || echo "000")
if [ "$HTTP_CODE" = "200" ]; then
    print_success "Aplicación web responde (HTTP $HTTP_CODE)"
else
    print_error "Aplicación web no responde (HTTP $HTTP_CODE)"
    print_solution "Espera unos segundos y refresca la página, o ejecuta: ./scripts/start-project.sh"
fi

echo ""
echo "6. Verificando logs del contenedor..."
RECENT_ERRORS=$(docker compose -f docker-compose.desarrollo.yml logs saltoestudia-dev | grep -E "(ERROR|Exception)" | tail -3)
if [ -n "$RECENT_ERRORS" ]; then
    print_warning "Errores recientes en logs:"
    echo "$RECENT_ERRORS"
    print_solution "Revisa los logs completos: docker compose -f docker-compose.desarrollo.yml logs saltoestudia-dev"
else
    print_success "No hay errores recientes en logs"
fi

# ================================================================================
# PROBLEMAS COMUNES Y SOLUCIONES
# ================================================================================

echo ""
echo "📋 PROBLEMAS COMUNES Y SOLUCIONES"
echo "=================================="

echo ""
echo "🔴 PROBLEMA: 'No such table: curso' o 'No such table: instituciones'"
echo "   CAUSA: Base de datos no creada o migraciones no aplicadas"
echo "   SOLUCIÓN: ./scripts/start-project.sh"
echo ""

echo "🔴 PROBLEMA: 'Permission denied' en data/"
echo "   CAUSA: Permisos incorrectos en carpeta data/"
echo "   SOLUCIÓN: sudo chown -R root:root data/ && sudo chmod -R 777 data/"
echo ""

echo "🔴 PROBLEMA: Contenedor no inicia"
echo "   CAUSA: Puerto ocupado o Docker no ejecutándose"
echo "   SOLUCIÓN: docker compose -f docker-compose.desarrollo.yml down && ./scripts/start-project.sh"
echo ""

echo "🔴 PROBLEMA: Página web no carga"
echo "   CAUSA: Aplicación aún iniciando o cache del navegador"
echo "   SOLUCIÓN: Espera 30 segundos y refresca (Ctrl+F5) o abre en modo incógnito"
echo ""

echo "🔴 PROBLEMA: No se ven cursos/instituciones"
echo "   CAUSA: Cache de la aplicación o datos no cargados"
echo "   SOLUCIÓN: Refresca la página o ejecuta: ./scripts/start-project.sh"
echo ""

# ================================================================================
# COMANDOS ÚTILES
# ================================================================================

echo ""
echo "🔧 COMANDOS ÚTILES"
echo "=================="
echo ""
echo "📊 Ver estado del contenedor:"
echo "   docker compose -f docker-compose.desarrollo.yml ps"
echo ""
echo "📋 Ver logs en tiempo real:"
echo "   docker compose -f docker-compose.desarrollo.yml logs -f"
echo ""
echo "🔄 Reiniciar aplicación:"
echo "   ./scripts/start-project.sh"
echo ""
echo "🛑 Detener aplicación:"
echo "   docker compose -f docker-compose.desarrollo.yml down"
echo ""
echo "🗄️ Verificar base de datos:"
echo "   docker compose -f docker-compose.desarrollo.yml exec saltoestudia-dev python -c \"from saltoestudia.database import obtener_cursos; print(f'Cursos: {len(obtener_cursos())}')\""
echo ""
echo "🌐 Acceso a la aplicación:"
echo "   Frontend: http://localhost:3000"
echo "   Backend: http://localhost:8000"
echo ""

print_success "Diagnóstico completado. Si hay problemas, usa las soluciones sugeridas arriba." 