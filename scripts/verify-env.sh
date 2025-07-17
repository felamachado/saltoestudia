#!/bin/bash

# Script para verificar la configuración del archivo .env
# Uso: ./scripts/verify-env.sh [local|production]

echo "🔍 Verificando configuración del archivo .env..."

# Verificar si existe el archivo .env
if [ ! -f ".env" ]; then
    echo "❌ Archivo .env no encontrado"
    echo "💡 Copia env.example como .env y configúralo"
    exit 1
fi

echo "✅ Archivo .env encontrado"

# Función para verificar configuración local
verify_local() {
    echo "🔧 Verificando configuración LOCAL (SQLite)..."
    
    if grep -q "DATABASE_URL=sqlite:///data/saltoestudia.db" .env; then
        echo "✅ DATABASE_URL configurado para SQLite"
    else
        echo "❌ DATABASE_URL no configurado para SQLite"
        echo "💡 Debe ser: DATABASE_URL=sqlite:///data/saltoestudia.db"
    fi
    
    if grep -q "REFLEX_DB_URL=sqlite:///reflex.db" .env; then
        echo "✅ REFLEX_DB_URL configurado para SQLite"
    else
        echo "❌ REFLEX_DB_URL no configurado para SQLite"
        echo "💡 Debe ser: REFLEX_DB_URL=sqlite:///reflex.db"
    fi
}

# Función para verificar configuración de producción
verify_production() {
    echo "🚀 Verificando configuración PRODUCCIÓN (PostgreSQL)..."
    
    if grep -q "DATABASE_URL=postgresql://" .env; then
        echo "✅ DATABASE_URL configurado para PostgreSQL"
    else
        echo "❌ DATABASE_URL no configurado para PostgreSQL"
        echo "💡 Debe ser: DATABASE_URL=postgresql://saltoestudia:password@postgres:5432/saltoestudia"
    fi
    
    if grep -q "REFLEX_DB_URL=postgresql://" .env; then
        echo "✅ REFLEX_DB_URL configurado para PostgreSQL"
    else
        echo "❌ REFLEX_DB_URL no configurado para PostgreSQL"
        echo "💡 Debe ser: REFLEX_DB_URL=postgresql://saltoestudia:password@postgres:5432/saltoestudia"
    fi
    
    if grep -q "DB_PASSWORD=" .env; then
        echo "✅ DB_PASSWORD configurado"
    else
        echo "❌ DB_PASSWORD no configurado"
        echo "💡 Agregar: DB_PASSWORD=tu_password_seguro"
    fi
    
    if grep -q "REFLEX_ENV=production" .env; then
        echo "✅ REFLEX_ENV configurado para producción"
    else
        echo "❌ REFLEX_ENV no configurado para producción"
        echo "💡 Agregar: REFLEX_ENV=production"
    fi
}

# Verificar contraseñas de usuarios
verify_passwords() {
    echo "🔑 Verificando contraseñas de usuarios..."
    
    required_passwords=(
        "DEFAULT_SEED_PASSWORD"
        "CENUR_PASSWORD"
        "IAE_PASSWORD"
        "CATALINA_PASSWORD"
        "ADMINISTRACION_PASSWORD"
        "AGRARIA_PASSWORD"
    )
    
    for password_var in "${required_passwords[@]}"; do
        if grep -q "^${password_var}=" .env; then
            echo "✅ $password_var configurado"
        else
            echo "❌ $password_var no configurado"
        fi
    done
}

# Lógica principal
case "${1:-local}" in
    "local")
        verify_local
        verify_passwords
        ;;
    "production")
        verify_production
        verify_passwords
        ;;
    *)
        echo "Uso: $0 [local|production]"
        echo "  local: Verifica configuración para desarrollo local"
        echo "  production: Verifica configuración para producción"
        exit 1
        ;;
esac

echo ""
echo "📋 Resumen de verificación completada"
echo "💡 Para más información, consulta:"
echo "   - DEPLOY-VPS.md"
echo "   - TROUBLESHOOTING.md"
echo "   - CONFIGURATION.md" 