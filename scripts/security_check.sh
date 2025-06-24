#!/bin/bash

# ========================================
# SCRIPT DE VERIFICACIÓN DE SEGURIDAD
# ========================================
# Este script verifica que no haya información sensible
# antes de hacer commit a GitHub
#
# Uso: ./scripts/security_check.sh
# ========================================

echo "🔐 VERIFICACIÓN DE SEGURIDAD - SALTO ESTUDIA"
echo "=============================================="

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Contadores
ERRORS=0
WARNINGS=0

# Función para mostrar errores
error() {
    echo -e "${RED}❌ ERROR: $1${NC}"
    ERRORS=$((ERRORS + 1))
}

# Función para mostrar advertencias
warning() {
    echo -e "${YELLOW}⚠️  ADVERTENCIA: $1${NC}"
    WARNINGS=$((WARNINGS + 1))
}

# Función para mostrar éxito
success() {
    echo -e "${GREEN}✅ $1${NC}"
}

echo ""
echo "1. Verificando archivos .env..."

# Verificar que no existe .env en el repositorio
if [ -f ".env" ]; then
    error "Archivo .env encontrado. Este archivo NO debe estar en el repositorio."
    echo "   Solución: git rm --cached .env"
fi

# Verificar que existe .env.example
if [ ! -f ".env.example" ]; then
    error "Archivo .env.example no encontrado. Debe existir como plantilla."
else
    success "Archivo .env.example encontrado"
fi

echo ""
echo "2. Verificando .gitignore..."

# Verificar que .env está en .gitignore
if ! grep -q "^\.env$" .gitignore; then
    error ".env no está en .gitignore"
else
    success ".env está correctamente excluido en .gitignore"
fi

echo ""
echo "3. Buscando credenciales hardcodeadas..."

# Buscar patrones de contraseñas hardcodeadas
if grep -r -i --exclude-dir=.git --exclude-dir=.web --exclude-dir=node_modules --exclude-dir=.bun \
    -E "(password|secret|key)\s*=\s*['\"][^'\"]{8,}" . 2>/dev/null; then
    warning "Posibles credenciales hardcodeadas encontradas. Revisa los archivos anteriores."
fi

# Buscar tokens de API o claves
if grep -r -i --exclude-dir=.git --exclude-dir=.web --exclude-dir=node_modules --exclude-dir=.bun \
    -E "(api_key|access_token|secret_key)\s*=\s*['\"][^'\"]{16,}" . 2>/dev/null; then
    warning "Posibles tokens de API encontrados. Revisa los archivos anteriores."
fi

echo ""
echo "4. Verificando archivos que no deben estar en el repositorio..."

# Lista de archivos/directorios que no deben estar
FORBIDDEN_FILES=(
    "reflex.db"
    "*.sqlite"
    "*.sqlite3"
    ".env"
    "node_modules"
    "__pycache__"
    "*.pyc"
    ".DS_Store"
    "Thumbs.db"
)

for pattern in "${FORBIDDEN_FILES[@]}"; do
    if find . -name "$pattern" -not -path "./.git/*" 2>/dev/null | grep -q .; then
        warning "Archivos que coinciden con '$pattern' encontrados"
        find . -name "$pattern" -not -path "./.git/*" 2>/dev/null | head -5
    fi
done

echo ""
echo "5. Verificando configuración de Docker Compose..."

# Verificar configuración de Docker Compose
if [ -f "docker-compose.yml" ]; then
    success "docker-compose.yml encontrado"
fi

echo ""
echo "6. Verificando archivos de Git..."

# Verificar archivos staged
STAGED_FILES=$(git diff --cached --name-only 2>/dev/null || echo "")
if [ -n "$STAGED_FILES" ]; then
    echo "Archivos preparados para commit:"
    echo "$STAGED_FILES" | while read -r file; do
        if [[ "$file" == *.env ]]; then
            error "Archivo .env está preparado para commit: $file"
        else
            echo "  📄 $file"
        fi
    done
else
    echo "No hay archivos preparados para commit"
fi

echo ""
echo "=============================================="
echo "📊 RESUMEN DE VERIFICACIÓN:"

if [ $ERRORS -gt 0 ]; then
    echo -e "${RED}❌ $ERRORS errores críticos encontrados${NC}"
    echo -e "${RED}🚫 NO ES SEGURO hacer commit hasta resolver los errores${NC}"
    echo ""
    echo "💡 Acciones recomendadas:"
    echo "   1. Resolver todos los errores listados arriba"
    echo "   2. Ejecutar: git rm --cached .env (si existe)"
    echo "   3. Verificar que .env esté en .gitignore"
    echo "   4. Ejecutar este script nuevamente"
    exit 1
elif [ $WARNINGS -gt 0 ]; then
    echo -e "${YELLOW}⚠️  $WARNINGS advertencias encontradas${NC}"
    echo -e "${YELLOW}⚠️  Revisa las advertencias antes de continuar${NC}"
    echo ""
    echo "💡 Es recomendable resolver las advertencias, pero puedes continuar."
    exit 2
else
    echo -e "${GREEN}✅ ¡VERIFICACIÓN EXITOSA!${NC}"
    echo -e "${GREEN}🚀 Es seguro hacer commit a GitHub${NC}"
    echo ""
    echo "🎉 Tu proyecto está listo para ser compartido de forma segura."
    exit 0
fi 