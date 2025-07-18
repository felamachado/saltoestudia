#!/bin/bash

# ================================================================================
# SCRIPT DE VERIFICACIÓN: DOCKER ONLY
# ================================================================================
# 
# Este script verifica que el proyecto se ejecute solo en Docker
# y muestra advertencias si se intenta usar Reflex nativo
# ================================================================================

set -e

# Colores para output
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para mostrar mensaje de error
show_error() {
    echo -e "${RED}"
    echo "=================================================================================="
    echo "🚫 ERROR: INTENTO DE EJECUTAR REFLEX NATIVO"
    echo "=================================================================================="
    echo ""
    echo "Este proyecto SOLO se ejecuta en Docker."
    echo ""
    echo "❌ NO ejecutes:"
    echo "   reflex run"
    echo "   reflex run --loglevel debug"
    echo "   reflex run --frontend-only"
    echo "   reflex run --backend-only"
    echo ""
    echo "✅ EJECUTA SIEMPRE:"
    echo "   docker compose -f docker-compose.desarrollo.yml up -d"
    echo ""
    echo "📖 Para más información, consulta:"
    echo "   - DOCKER-ONLY.md"
    echo "   - README.md"
    echo ""
    echo "🛠️  Si necesitas ayuda:"
    echo "   ./scripts/start-project.sh docker"
    echo "=================================================================================="
    echo -e "${NC}"
    exit 1
}

# Función para mostrar mensaje de éxito
show_success() {
    echo -e "${GREEN}"
    echo "=================================================================================="
    echo "✅ VERIFICACIÓN EXITOSA: DOCKER ONLY"
    echo "=================================================================================="
    echo ""
    echo "El proyecto está configurado correctamente para Docker."
    echo ""
    echo "🚀 Para iniciar la aplicación:"
    echo "   docker compose -f docker-compose.desarrollo.yml up -d"
    echo ""
    echo "📖 Documentación:"
    echo "   - DOCKER-ONLY.md"
    echo "   - README.md"
    echo "=================================================================================="
    echo -e "${NC}"
}

# Función para verificar si Docker está instalado
check_docker() {
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}❌ Docker no está instalado${NC}"
        echo "Instala Docker antes de continuar:"
        echo "https://docs.docker.com/get-docker/"
        exit 1
    fi
    
    if ! docker info &> /dev/null; then
        echo -e "${RED}❌ Docker no está ejecutándose${NC}"
        echo "Inicia Docker antes de continuar."
        exit 1
    fi
    
    echo -e "${GREEN}✅ Docker está instalado y ejecutándose${NC}"
}

# Función para verificar si docker-compose está disponible
check_docker_compose() {
    if command -v docker-compose &> /dev/null; then
        echo -e "${GREEN}✅ docker-compose está disponible${NC}"
        return 0
    elif docker compose version &> /dev/null; then
        echo -e "${GREEN}✅ docker compose está disponible${NC}"
        return 0
    else
        echo -e "${RED}❌ docker-compose no está disponible${NC}"
        echo "Instala docker-compose antes de continuar."
        exit 1
    fi
}

# Función para verificar archivos de configuración
check_config_files() {
    local missing_files=()
    
    if [[ ! -f "docker-compose.desarrollo.yml" ]]; then
        missing_files+=("docker-compose.desarrollo.yml")
    fi
    
    if [[ ! -f "config-desarrollo.env" ]]; then
        missing_files+=("config-desarrollo.env")
    fi
    
    if [[ ! -f "DOCKER-ONLY.md" ]]; then
        missing_files+=("DOCKER-ONLY.md")
    fi
    
    if [[ ${#missing_files[@]} -gt 0 ]]; then
        echo -e "${RED}❌ Archivos de configuración faltantes:${NC}"
        for file in "${missing_files[@]}"; do
            echo "   - $file"
        done
        exit 1
    fi
    
    echo -e "${GREEN}✅ Todos los archivos de configuración están presentes${NC}"
}

# Función para verificar puertos
check_ports() {
    local ports=(3000 8000 5432)
    local occupied_ports=()
    
    for port in "${ports[@]}"; do
        if lsof -i :$port &> /dev/null; then
            occupied_ports+=("$port")
        fi
    done
    
    if [[ ${#occupied_ports[@]} -gt 0 ]]; then
        echo -e "${YELLOW}⚠️  Puertos ocupados:${NC}"
        for port in "${occupied_ports[@]}"; do
            echo "   - Puerto $port"
        done
        echo ""
        echo "Esto puede causar conflictos. Considera liberar estos puertos."
    else
        echo -e "${GREEN}✅ Todos los puertos necesarios están libres${NC}"
    fi
}

# Función principal
main() {
    echo -e "${BLUE}"
    echo "=================================================================================="
    echo "🔍 VERIFICANDO CONFIGURACIÓN DOCKER ONLY"
    echo "=================================================================================="
    echo -e "${NC}"
    
    # Verificar si se está intentando ejecutar Reflex nativo
    if [[ "$1" == "reflex" ]] || [[ "$1" == "reflex run" ]]; then
        show_error
    fi
    
    # Verificaciones
    check_docker
    check_docker_compose
    check_config_files
    check_ports
    
    echo ""
    show_success
}

# Ejecutar función principal con argumentos
main "$@" 