#!/bin/bash

# Script para verificar que todo esté funcionando correctamente
# Uso: ./scripts/verify-setup.sh

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para imprimir mensajes
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

echo "🔍 Verificando configuración de Salto Estudia..."
echo "================================================"
echo ""

# Contador de problemas
PROBLEMS=0

# 1. Verificar base de datos
print_status "1. Verificando base de datos..."
if [ -f "data/saltoestudia.db" ]; then
    print_success "✅ Base de datos existe"
    
    # Verificar que tiene datos
    CURSOS_COUNT=$(python3 -c "import sqlite3; conn = sqlite3.connect('data/saltoestudia.db'); cursor = conn.cursor(); cursor.execute('SELECT COUNT(*) FROM curso'); print(cursor.fetchone()[0]); conn.close()" 2>/dev/null | tail -1 || echo "0")
    INSTITUCIONES_COUNT=$(python3 -c "import sqlite3; conn = sqlite3.connect('data/saltoestudia.db'); cursor = conn.cursor(); cursor.execute('SELECT COUNT(*) FROM instituciones'); print(cursor.fetchone()[0]); conn.close()" 2>/dev/null | tail -1 || echo "0")
    
    if [ "$CURSOS_COUNT" -gt 0 ] 2>/dev/null && [ "$INSTITUCIONES_COUNT" -gt 0 ] 2>/dev/null; then
        print_success "✅ Base de datos tiene datos: $CURSOS_COUNT cursos, $INSTITUCIONES_COUNT instituciones"
    else
        print_error "❌ Base de datos vacía o corrupta"
        PROBLEMS=$((PROBLEMS + 1))
    fi
else
    print_error "❌ Base de datos no existe"
    PROBLEMS=$((PROBLEMS + 1))
fi

# 2. Verificar permisos
print_status "2. Verificando permisos..."
if [ -r "data/saltoestudia.db" ] && [ -w "data/saltoestudia.db" ]; then
    print_success "✅ Permisos correctos"
else
    print_error "❌ Problema de permisos"
    print_warning "Ejecutar: chmod 666 data/saltoestudia.db"
    PROBLEMS=$((PROBLEMS + 1))
fi

# 3. Verificar Docker
print_status "3. Verificando Docker..."
if command -v docker &> /dev/null; then
    print_success "✅ Docker instalado"
    
    # Verificar que Docker está ejecutándose
    if docker info &> /dev/null; then
        print_success "✅ Docker ejecutándose"
        
        # Verificar contenedor
        if docker compose -f docker-compose.dev.yml ps | grep -q "Up"; then
            print_success "✅ Contenedor ejecutándose"
            
            # Verificar que la aplicación responde
            if curl -s http://localhost:3000 > /dev/null 2>&1; then
                print_success "✅ Aplicación web respondiendo"
                
                # Verificar datos desde el contenedor
                CONTAINER_CURSOS=$(docker exec saltoestudia-dev-app python3 -c "from saltoestudia.database import obtener_cursos; print(len(obtener_cursos()))" 2>/dev/null | tail -1 || echo "0")
                if [ "$CONTAINER_CURSOS" -gt 0 ] 2>/dev/null; then
                    print_success "✅ Datos cargados en contenedor: $CONTAINER_CURSOS cursos"
                else
                    print_error "❌ No hay datos en el contenedor"
                    PROBLEMS=$((PROBLEMS + 1))
                fi
            else
                print_warning "⚠️  Aplicación web no responde (puede estar iniciando)"
            fi
        else
            print_warning "⚠️  Contenedor no ejecutándose"
            print_status "Ejecutar: ./scripts/start-project.sh docker"
        fi
    else
        print_error "❌ Docker no está ejecutándose"
        PROBLEMS=$((PROBLEMS + 1))
    fi
else
    print_warning "⚠️  Docker no instalado"
    print_status "Puedes usar modo local: ./scripts/start-project.sh local"
fi

# 4. Verificar puertos
print_status "4. Verificando puertos..."
if lsof -i :3000 > /dev/null 2>&1; then
    print_success "✅ Puerto 3000 disponible"
else
    print_warning "⚠️  Puerto 3000 ocupado"
fi

if lsof -i :8000 > /dev/null 2>&1; then
    print_success "✅ Puerto 8000 disponible"
else
    print_warning "⚠️  Puerto 8000 ocupado"
fi

# 5. Verificar archivos críticos
print_status "5. Verificando archivos críticos..."
CRITICAL_FILES=("saltoestudia/database.py" "saltoestudia/state.py" "docker-compose.dev.yml" "requirements.txt")
for file in "${CRITICAL_FILES[@]}"; do
    if [ -f "$file" ]; then
        print_success "✅ $file existe"
    else
        print_error "❌ $file no existe"
        PROBLEMS=$((PROBLEMS + 1))
    fi
done

# 6. Verificar scripts
print_status "6. Verificando scripts..."
if [ -x "scripts/start-project.sh" ]; then
    print_success "✅ Script de inicio ejecutable"
else
    print_warning "⚠️  Script de inicio no ejecutable"
    print_status "Ejecutar: chmod +x scripts/start-project.sh"
fi

# Resumen final
echo ""
echo "================================================"
echo "📊 RESUMEN DE VERIFICACIÓN"
echo "================================================"

if [ $PROBLEMS -eq 0 ]; then
    print_success "🎉 ¡Todo está funcionando correctamente!"
    echo ""
    echo "🌐 Acceso a la aplicación:"
    echo "   Frontend: http://localhost:3000"
    echo "   Backend:  http://localhost:8000"
    echo "   Admin:    http://localhost:3000/admin"
    echo ""
    echo "📚 Páginas disponibles:"
    echo "   Cursos:       http://localhost:3000/cursos"
    echo "   Instituciones: http://localhost:3000/instituciones"
    echo ""
    print_success "¡Tu entorno de desarrollo está listo! 🚀"
else
    print_error "❌ Se encontraron $PROBLEMS problema(s)"
    echo ""
    echo "🔧 Soluciones recomendadas:"
    echo "   1. Ejecutar: ./scripts/start-project.sh docker"
    echo "   2. Si persisten problemas, revisar logs:"
    echo "      docker logs saltoestudia-dev-app -f"
    echo "   3. Para limpiar todo:"
    echo "      docker compose -f docker-compose.dev.yml down"
    echo "      ./scripts/start-project.sh docker"
    echo ""
    print_warning "Revisa la documentación en TROUBLESHOOTING.md"
fi

echo ""
echo "🔧 Comandos útiles:"
echo "   Iniciar:     ./scripts/start-project.sh docker"
echo "   Ver logs:    docker logs saltoestudia-dev-app -f"
echo "   Detener:     docker compose -f docker-compose.dev.yml down"
echo "   Verificar:   ./scripts/verify-setup.sh"
echo ""

exit $PROBLEMS 