#!/bin/bash

# Script para iniciar Salto Estudia en modo Docker
# Uso: ./scripts/start-project.sh [docker|help]

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

# Función para iniciar en modo Docker
start_docker() {
    print_status "Iniciando Salto Estudia en modo DOCKER..."
    
    # Verificar que Docker está instalado
    if ! command -v docker &> /dev/null; then
        print_error "Docker no está instalado"
        exit 1
    fi
    
    # Verificar que docker-compose está disponible
    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
        print_error "docker-compose no está disponible"
        exit 1
    fi
    
    # Detener contenedores existentes
    print_status "Deteniendo contenedores existentes..."
    docker compose -f docker-compose.desarrollo.yml down 2>/dev/null || true
    
    # Construir y levantar contenedores
    print_status "Construyendo y levantando contenedores..."
    docker compose -f docker-compose.desarrollo.yml up -d --build
    
    # Esperar a que la aplicación esté lista
    print_status "Esperando a que la aplicación esté lista..."
    sleep 15
    
    # Verificar que la aplicación está funcionando
    if curl -s http://localhost:3000 > /dev/null 2>&1; then
        print_success "¡Aplicación iniciada correctamente!"
        print_status "Frontend: http://localhost:3000"
        print_status "Backend:  http://localhost:8000"
        print_status "Para ver logs: docker logs saltoestudia-dev-app -f"
        print_status "Para detener: docker compose -f docker-compose.desarrollo.yml down"
    else
        print_error "La aplicación no está respondiendo"
        print_status "Verificando logs..."
        docker logs saltoestudia-dev-app --tail 20
        exit 1
    fi
}

# Función para mostrar ayuda
show_help() {
    echo "Script para iniciar Salto Estudia"
    echo ""
    echo "Uso: $0 [OPCIÓN]"
    echo ""
    echo "Opciones:"
    echo "  docker    Iniciar en modo Docker (recomendado)"
    echo "  help      Mostrar esta ayuda"
    echo ""
    echo "Ejemplos:"
    echo "  $0 docker  # Inicia en modo Docker"
    echo ""
    echo "Nota: Este proyecto se ejecuta exclusivamente en Docker"
}

# Función principal
main() {
    echo "🚀 SALTO ESTUDIA - SCRIPT DE INICIO"
    echo "===================================="
    echo ""
    
    case "${1:-docker}" in
        "docker")
            start_docker
            ;;
        "help"|"-h"|"--help")
            show_help
            ;;
        *)
            print_warning "Opción '$1' no válida. Usando Docker por defecto."
            start_docker
            ;;
    esac
}

# Ejecutar función principal
main "$@" 