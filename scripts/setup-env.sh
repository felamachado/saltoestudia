#!/bin/bash

# Script para configurar el entorno de desarrollo o producción
# Uso: ./scripts/setup-env.sh [desarrollo|produccion]

set -e

ENV=${1:-desarrollo}

echo "🔧 Configurando entorno: $ENV"

case $ENV in
    "desarrollo"|"dev")
        echo "📁 Configurando entorno de desarrollo..."
        
        # Copiar configuración de desarrollo
        if [ -f "docker-compose.desarrollo.yml" ]; then
            cp docker-compose.desarrollo.yml docker-compose.yml
            echo "✅ docker-compose.yml configurado para desarrollo"
        else
            echo "❌ Error: docker-compose.desarrollo.yml no encontrado"
            exit 1
        fi
        
        # Copiar variables de entorno de desarrollo
        if [ -f "config-desarrollo.env" ]; then
            cp config-desarrollo.env .env
            echo "✅ .env configurado para desarrollo"
        else
            echo "❌ Error: config-desarrollo.env no encontrado"
            exit 1
        fi
        
        echo "🎯 Entorno de desarrollo configurado:"
        echo "   - Dominio: desarrollo.saltoestudia.infra.com.uy"
        echo "   - Contenedor: saltoestudia-dev-app"
        echo "   - Configuración: docker-compose.desarrollo.yml"
        ;;
        
    "produccion"|"prod")
        echo "📁 Configurando entorno de producción..."
        
        # Usar configuración de producción (docker-compose.yml original)
        if [ -f "docker-compose.yml" ]; then
            echo "✅ docker-compose.yml configurado para producción"
        else
            echo "❌ Error: docker-compose.yml no encontrado"
            exit 1
        fi
        
        # Verificar que .env existe y no es el de desarrollo
        if [ -f ".env" ]; then
            if grep -q "dev_password_123" .env; then
                echo "⚠️  ADVERTENCIA: .env contiene contraseñas de desarrollo"
                echo "   Configura contraseñas seguras para producción"
            else
                echo "✅ .env configurado para producción"
            fi
        else
            echo "❌ Error: .env no encontrado"
            echo "   Copia .env.example a .env y configura las contraseñas"
            exit 1
        fi
        
        echo "🎯 Entorno de producción configurado:"
        echo "   - Dominio: saltoestudia.infra.com.uy"
        echo "   - Contenedor: saltoestudia-app"
        echo "   - Configuración: docker-compose.yml"
        ;;
        
    *)
        echo "❌ Error: Entorno '$ENV' no válido"
        echo "   Uso: $0 [desarrollo|produccion]"
        echo "   Ejemplos:"
        echo "     $0 desarrollo"
        echo "     $0 produccion"
        exit 1
        ;;
esac

echo ""
echo "🚀 Para iniciar la aplicación:"
echo "   docker compose up -d"
echo ""
echo "📊 Para ver logs:"
echo "   docker compose logs -f" 