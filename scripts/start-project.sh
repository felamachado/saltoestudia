#!/bin/bash

# Script para iniciar Salto Estudia en modo local o Docker
# Uso: ./scripts/start-project.sh [local|docker]

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

# Función para limpiar puertos
clean_ports() {
    print_status "Limpiando puertos 3000 y 8000..."
    pkill -f reflex || true
    pkill -f "bun run dev" || true
    lsof -ti :3000 | xargs -r kill -9 2>/dev/null || true
    lsof -ti :8000 | xargs -r kill -9 2>/dev/null || true
    sleep 2
    print_success "Puertos limpiados"
}

# Función para verificar dependencias
check_dependencies() {
    print_status "Verificando dependencias..."
    
    if ! command -v python3 &> /dev/null; then
        print_error "Python3 no está instalado"
        exit 1
    fi
    
    if ! command -v pip &> /dev/null; then
        print_error "pip no está instalado"
        exit 1
    fi
    
    print_success "Dependencias verificadas"
}

# Función para instalar dependencias
install_dependencies() {
    print_status "Instalando dependencias de Python..."
    pip install -r requirements.txt
    print_success "Dependencias instaladas"
}

# Función para iniciar en modo local
start_local() {
    print_status "Iniciando Salto Estudia en modo LOCAL..."
    
    # Limpiar puertos
    clean_ports
    
    # Verificar que la base de datos existe
    if [ ! -f "data/saltoestudia.db" ]; then
        print_warning "Base de datos no encontrada. Creando..."
        python3 init_db.py
        python3 seed.py
    fi
    
    # Verificar dependencias
    check_dependencies
    
    # Instalar dependencias si es necesario
    if [ ! -d ".venv" ] && [ ! -d "venv" ]; then
        install_dependencies
    fi
    
    print_success "Iniciando aplicación local..."
    print_status "Frontend: http://localhost:3000"
    print_status "Backend:  http://localhost:8000"
    print_status "Presiona Ctrl+C para detener"
    echo ""
    
    # Iniciar Reflex
    reflex run --backend-host 0.0.0.0 --backend-port 8000 --frontend-port 3000
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
    docker compose -f docker-compose.dev.yml down 2>/dev/null || true
    
    # Construir y levantar contenedores
    print_status "Construyendo y levantando contenedores..."
    docker compose -f docker-compose.dev.yml up -d --build
    
    # Esperar a que la aplicación esté lista
    print_status "Esperando a que la aplicación esté lista..."
    sleep 15
    
    # Verificar que la aplicación está funcionando
    if curl -s http://localhost:3000 > /dev/null 2>&1; then
        print_success "¡Aplicación iniciada correctamente!"
        print_status "Frontend: http://localhost:3000"
        print_status "Backend:  http://localhost:8000"
        print_status "Para ver logs: docker logs saltoestudia-dev-app -f"
        print_status "Para detener: docker compose -f docker-compose.dev.yml down"
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
    echo "  local     Iniciar en modo local (sin Docker)"
    echo "  docker    Iniciar en modo Docker (recomendado)"
    echo "  help      Mostrar esta ayuda"
    echo ""
    echo "Ejemplos:"
    echo "  $0 local   # Inicia en modo local"
    echo "  $0 docker  # Inicia en modo Docker"
    echo ""
    echo "Nota: Si no se especifica opción, se usa Docker por defecto"
}

# Función principal
main() {
    echo "🚀 SALTO ESTUDIA - SCRIPT DE INICIO"
    echo "===================================="
    echo ""
    
    case "${1:-docker}" in
        "local")
            start_local
            ;;
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