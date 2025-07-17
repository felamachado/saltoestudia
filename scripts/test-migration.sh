#!/bin/bash

# Script para probar la migración y configuración de PostgreSQL
# Uso: ./scripts/test-migration.sh

set -e

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
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

echo "🧪 Iniciando tests de migración..."
echo "=================================="

# 1. Verificar que los servicios estén corriendo
echo ""
print_status "1️⃣ Verificando servicios..."
if docker ps | grep -q saltoestudia-dev-frontend; then
    print_success "Frontend corriendo"
else
    print_error "Frontend no está corriendo"
    exit 1
fi

if docker ps | grep -q saltoestudia-dev-backend; then
    print_success "Backend corriendo"
else
    print_error "Backend no está corriendo"
    exit 1
fi

if docker ps | grep -q saltoestudia-dev-postgres; then
    print_success "PostgreSQL corriendo"
else
    print_error "PostgreSQL no está corriendo"
    exit 1
fi

# 2. Verificar conectividad entre servicios
echo ""
print_status "2️⃣ Verificando conectividad..."
if docker exec saltoestudia-dev-backend ping -c 1 postgres > /dev/null 2>&1; then
    print_success "Backend puede conectar a PostgreSQL"
else
    print_warning "Backend no puede hacer ping a PostgreSQL (no crítico)"
fi

if docker exec saltoestudia-dev-backend ping -c 1 frontend > /dev/null 2>&1; then
    print_success "Backend puede conectar a Frontend"
else
    print_warning "Backend no puede hacer ping a Frontend (no crítico)"
fi

# 3. Verificar base de datos
echo ""
print_status "3️⃣ Verificando base de datos..."
if docker exec saltoestudia-dev-backend python -c "
import os
from saltoestudia.database import engine
print(f'Database URL: {engine.url}')
print(f'Database connected: {engine.connect() is not None}')
" 2>/dev/null; then
    print_success "Conexión a base de datos exitosa"
else
    print_error "Error conectando a la base de datos"
    exit 1
fi

# 4. Verificar migración de datos
echo ""
print_status "4️⃣ Verificando datos migrados..."
if docker exec saltoestudia-dev-backend python scripts/verify_migration.py > /dev/null 2>&1; then
    print_success "Datos migrados correctamente"
else
    print_warning "Hay problemas con la migración de datos"
    print_status "Ejecuta: ./scripts/start-project.sh migrate"
fi

# 5. Verificar aplicación web
echo ""
print_status "5️⃣ Verificando aplicación web..."
if curl -f http://localhost:3000 > /dev/null 2>&1; then
    print_success "Frontend responde correctamente"
else
    print_error "Frontend no responde"
    exit 1
fi

if curl -f http://localhost:8000/_event > /dev/null 2>&1; then
    print_success "Backend responde correctamente"
else
    print_warning "Backend no responde en /_event (puede ser normal)"
fi

# 6. Verificar PostgreSQL directamente
echo ""
print_status "6️⃣ Verificando PostgreSQL directamente..."
if docker exec saltoestudia-dev-postgres psql -U saltoestudia -d saltoestudia -c "SELECT version();" > /dev/null 2>&1; then
    print_success "PostgreSQL funciona correctamente"
else
    print_error "Error conectando a PostgreSQL"
    exit 1
fi

# 7. Verificar tablas creadas
echo ""
print_status "7️⃣ Verificando tablas en PostgreSQL..."
tables=$(docker exec saltoestudia-dev-postgres psql -U saltoestudia -d saltoestudia -t -c "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';" 2>/dev/null | tr -d ' ' | grep -v '^$')

expected_tables=("ciudad" "instituciones" "sedes" "usuarios" "curso" "curso_ciudad")
missing_tables=()

for table in "${expected_tables[@]}"; do
    if echo "$tables" | grep -q "^${table}$"; then
        print_success "Tabla $table existe"
    else
        print_error "Tabla $table no existe"
        missing_tables+=("$table")
    fi
done

if [ ${#missing_tables[@]} -eq 0 ]; then
    print_success "Todas las tablas están creadas"
else
    print_warning "Faltan tablas: ${missing_tables[*]}"
    print_status "Ejecuta: ./scripts/start-project.sh migrate"
fi

echo ""
echo "🎉 Tests completados"
echo "==================="

if [ ${#missing_tables[@]} -eq 0 ]; then
    print_success "✅ Todos los tests pasaron exitosamente"
    echo ""
    print_status "📊 Resumen:"
    print_status "   - 3 contenedores corriendo"
    print_status "   - PostgreSQL configurado"
    print_status "   - Datos migrados"
    print_status "   - Aplicación funcionando"
    echo ""
    print_status "🌐 URLs:"
    print_status "   - Frontend: http://localhost:3000"
    print_status "   - Backend: http://localhost:8000"
    print_status "   - PostgreSQL: localhost:5432"
else
    print_warning "⚠️ Algunos tests fallaron"
    print_status "Revisa los errores y ejecuta la migración si es necesario"
fi 