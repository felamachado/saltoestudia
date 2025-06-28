#!/bin/bash

# =============================================================================
# Script de Instalación de Alias Global para Salto Estudia
# =============================================================================
# 
# Este script instala un alias global que permite arrancar la aplicación
# desde cualquier carpeta usando simplemente: saltoestudia
#
# Uso: ./install-alias.sh
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

print_status "🔧 Instalando alias global para Salto Estudia..."
echo ""

# Obtener el directorio del proyecto
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Verificar que estamos en el directorio correcto
if [ ! -f "$PROJECT_DIR/rxconfig.py" ]; then
    print_error "❌ Este script debe ejecutarse desde la carpeta raíz del proyecto Salto Estudia"
    print_error "❌ Directorio actual: $PROJECT_DIR"
    echo ""
    print_status "💡 Solución:"
    print_status "   Navega a la carpeta del proyecto:"
    print_status "   cd ~/Escritorio/Proyectos/saltoestudia"
    print_status "   ./install-alias.sh"
    echo ""
    exit 1
fi

print_success "✅ Directorio del proyecto verificado: $PROJECT_DIR"
echo ""

# Determinar el archivo de configuración del shell
SHELL_CONFIG=""
if [ -n "$ZSH_VERSION" ]; then
    SHELL_CONFIG="$HOME/.zshrc"
elif [ -n "$BASH_VERSION" ]; then
    SHELL_CONFIG="$HOME/.bashrc"
else
    # Intentar detectar automáticamente
    if [ -f "$HOME/.zshrc" ]; then
        SHELL_CONFIG="$HOME/.zshrc"
    elif [ -f "$HOME/.bashrc" ]; then
        SHELL_CONFIG="$HOME/.bashrc"
    else
        print_error "❌ No se pudo determinar el archivo de configuración del shell"
        print_error "❌ Shell actual: $SHELL"
        echo ""
        print_status "💡 Solución manual:"
        print_status "   Agrega esta línea a tu archivo de configuración del shell (.bashrc, .zshrc, etc.):"
        print_status "   alias saltoestudia='$PROJECT_DIR/scripts/arrancar_app.sh'"
        echo ""
        exit 1
    fi
fi

print_status "📝 Archivo de configuración detectado: $SHELL_CONFIG"
echo ""

# Crear el alias
ALIAS_LINE="alias saltoestudia='$PROJECT_DIR/scripts/arrancar_app.sh'"

# Verificar si el alias ya existe
if grep -q "alias saltoestudia=" "$SHELL_CONFIG" 2>/dev/null; then
    print_warning "⚠️  El alias 'saltoestudia' ya existe en $SHELL_CONFIG"
    print_status "🔄 Actualizando el alias existente..."
    
    # Actualizar el alias existente
    if [[ "$OSTYPE" == "darwin"* ]]; then
        # macOS
        sed -i '' "s|alias saltoestudia=.*|$ALIAS_LINE|" "$SHELL_CONFIG"
    else
        # Linux
        sed -i "s|alias saltoestudia=.*|$ALIAS_LINE|" "$SHELL_CONFIG"
    fi
else
    print_status "➕ Agregando nuevo alias..."
    echo "" >> "$SHELL_CONFIG"
    echo "# Alias para Salto Estudia" >> "$SHELL_CONFIG"
    echo "$ALIAS_LINE" >> "$SHELL_CONFIG"
fi

print_success "✅ Alias instalado correctamente"
echo ""

# Recargar la configuración del shell
print_status "🔄 Recargando configuración del shell..."
if [ -n "$ZSH_VERSION" ]; then
    source "$SHELL_CONFIG" 2>/dev/null || true
elif [ -n "$BASH_VERSION" ]; then
    source "$SHELL_CONFIG" 2>/dev/null || true
fi

print_success "🎉 Instalación completada"
echo ""
print_status "📋 Resumen:"
print_status "   - Alias creado: saltoestudia"
print_status "   - Archivo modificado: $SHELL_CONFIG"
print_status "   - Ruta del proyecto: $PROJECT_DIR"
echo ""
print_status "✅ Ahora puedes usar el comando desde cualquier carpeta:"
print_status "   saltoestudia"
echo ""
print_status "💡 Si el comando no funciona inmediatamente, reinicia tu terminal o ejecuta:"
print_status "   source $SHELL_CONFIG"
echo "" 