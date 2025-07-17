#!/bin/bash

# Script para iniciar Salto Estudia en modo Docker con 3 contenedores
# Uso: ./scripts/start-project.sh [docker|production|stop|logs|postgres|migrate|verify|help]

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

# Función para verificar dependencias
check_dependencies() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker no está instalado"
        exit 1
    fi
    
    if ! docker compose version &> /dev/null; then
        print_error "docker compose no está disponible"
        exit 1
    fi
}

# Función para iniciar en modo desarrollo (3 contenedores)
start_development() {
    print_status "Iniciando Salto Estudia en modo DESARROLLO (3 contenedores + PostgreSQL)..."
    
    # Verificar que PostgreSQL esté listo
    print_status "Esperando que PostgreSQL esté listo..."
    docker compose -f docker-compose.desarrollo.yml up -d postgres
    
    # Esperar a que PostgreSQL esté saludable
    timeout=60
    while [ $timeout -gt 0 ]; do
        if docker exec saltoestudia-dev-postgres pg_isready -U saltoestudia > /dev/null 2>&1; then
            print_success "PostgreSQL está listo"
            break
        fi
        print_status "Esperando PostgreSQL... ($timeout segundos restantes)"
        sleep 5
        timeout=$((timeout - 5))
    done
    
    if [ $timeout -le 0 ]; then
        print_error "Timeout esperando PostgreSQL"
        exit 1
    fi
    
    # Iniciar el resto de servicios
    print_status "Iniciando frontend y backend..."
    docker compose -f docker-compose.desarrollo.yml up -d --build frontend backend
    
    # Esperar a que la aplicación esté lista
    print_status "Esperando a que la aplicación esté lista..."
    sleep 15
    
    # Verificar que la aplicación está funcionando
    if curl -s http://localhost:3000 > /dev/null 2>&1; then
        print_success "¡Aplicación iniciada correctamente!"
        print_status "Frontend: http://localhost:3000"
        print_status "Backend:  http://localhost:8000"
        print_status "PostgreSQL: localhost:5432"
        print_status ""
        print_status "Comandos útiles:"
        print_status "  Ver logs: $0 logs"
        print_status "  Conectar a DB: $0 postgres"
        print_status "  Detener: $0 stop"
    else
        print_error "La aplicación no está respondiendo"
        print_status "Verificando logs..."
        docker logs saltoestudia-dev-backend --tail 20
        exit 1
    fi
}

# Función para iniciar en modo producción
start_production() {
    print_status "Iniciando Salto Estudia en modo PRODUCCIÓN (3 contenedores + PostgreSQL)..."
    
    # Verificar variables de entorno
    if [ ! -f ".env" ]; then
        print_error "Archivo .env no encontrado"
        print_status "Copia env.example como .env y configura las credenciales"
        exit 1
    fi
    
    # Iniciar servicios
    docker compose up -d --build
    
    print_success "¡Servicios de producción iniciados!"
    print_status "URL: https://saltoestudia.infra.com.uy"
    print_status "PostgreSQL: Contenedor interno"
}

# Función para detener servicios
stop_services() {
    print_status "Deteniendo servicios..."
    docker compose -f docker-compose.desarrollo.yml down
    docker compose down
    print_success "Servicios detenidos"
}

# Función para mostrar logs
show_logs() {
    print_status "Mostrando logs en tiempo real..."
    docker compose -f docker-compose.desarrollo.yml logs -f
}

# Función para conectar a PostgreSQL
connect_postgres() {
    print_status "Conectando a PostgreSQL..."
    
    if docker ps | grep -q saltoestudia-dev-postgres; then
        docker exec -it saltoestudia-dev-postgres psql -U saltoestudia -d saltoestudia
    elif docker ps | grep -q saltoestudia-postgres; then
        docker exec -it saltoestudia-postgres psql -U saltoestudia -d saltoestudia
    else
        print_error "PostgreSQL no está corriendo"
        exit 1
    fi
}

# Función para migrar datos
migrate_data() {
    print_status "Iniciando migración de SQLite a PostgreSQL..."
    
    # Verificar que PostgreSQL esté corriendo
    if ! docker ps | grep -q saltoestudia-dev-postgres; then
        print_error "PostgreSQL no está corriendo. Ejecuta '$0 docker' primero"
        exit 1
    fi
    
    # Ejecutar migración
    docker exec saltoestudia-dev-backend python scripts/migrate_to_postgres.py
    
    if [ $? -eq 0 ]; then
        print_success "Migración completada"
        print_status "Ejecuta '$0 verify' para verificar los datos"
    else
        print_error "Error en la migración"
        exit 1
    fi
}

# Función para verificar migración
verify_migration() {
    print_status "Verificando migración de datos..."
    
    docker exec saltoestudia-dev-backend python scripts/verify_migration.py
    
    if [ $? -eq 0 ]; then
        print_success "Verificación exitosa"
    else
        print_error "Hay problemas en la migración"
        exit 1
    fi
}

# Función para mostrar ayuda
show_help() {
    echo "🚀 SALTO ESTUDIA - SCRIPT DE GESTIÓN"
    echo "===================================="
    echo ""
    echo "Uso: $0 [COMANDO]"
    echo ""
    echo "Comandos disponibles:"
    echo "  ${GREEN}docker${NC}      - Iniciar en desarrollo (3 contenedores + PostgreSQL)"
    echo "  ${GREEN}production${NC}  - Iniciar en producción (3 contenedores + PostgreSQL)"
    echo "  ${GREEN}stop${NC}        - Detener todos los servicios"
    echo "  ${GREEN}logs${NC}        - Mostrar logs en tiempo real"
    echo "  ${GREEN}postgres${NC}    - Conectar a PostgreSQL"
    echo "  ${GREEN}migrate${NC}     - Migrar datos de SQLite a PostgreSQL"
    echo "  ${GREEN}verify${NC}      - Verificar migración de datos"
    echo "  ${GREEN}help${NC}        - Mostrar esta ayuda"
    echo ""
    echo "Ejemplos:"
    echo "  $0 docker     # Inicia en desarrollo"
    echo "  $0 production # Inicia en producción"
    echo "  $0 migrate    # Migra datos a PostgreSQL"
    echo ""
    echo "Nota: Este proyecto usa 3 contenedores (frontend, backend, postgres)"
}

# Función principal
main() {
    echo "🚀 SALTO ESTUDIA - SCRIPT DE GESTIÓN"
    echo "===================================="
    echo ""
    
    # Verificar dependencias
    check_dependencies
    
    case "${1:-docker}" in
        "docker")
            start_development
            ;;
        "production")
            start_production
            ;;
        "stop")
            stop_services
            ;;
        "logs")
            show_logs
            ;;
        "postgres")
            connect_postgres
            ;;
        "migrate")
            migrate_data
            ;;
        "verify")
            verify_migration
            ;;
        "help"|"-h"|"--help")
            show_help
            ;;
        *)
            print_warning "Comando '$1' no válido. Usando 'docker' por defecto."
            start_development
            ;;
    esac
}

# Ejecutar función principal
main "$@" 