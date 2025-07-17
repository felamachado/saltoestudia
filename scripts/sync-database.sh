#!/bin/bash

# Script para sincronizar la base de datos en producción
# Este script resuelve el problema de que Reflex usa diferentes archivos de BD
# en desarrollo (data/saltoestudia.db) vs producción (reflex.db)

set -e

echo "🔄 Iniciando sincronización de base de datos..."

# Verificar si estamos en Docker (producción)
if [ -d "/app" ]; then
    echo "📍 Entorno detectado: Producción (Docker)"
    cd /app
else
    echo "📍 Entorno detectado: Desarrollo (Local)"
fi

# Verificar si existe la base de datos con datos
if [ -f "data/saltoestudia.db" ]; then
    echo "✅ Base de datos con datos encontrada en data/saltoestudia.db"
    
    # Verificar si la base de datos de Reflex existe y tiene datos
    if [ -f "reflex.db" ]; then
        echo "📊 Verificando contenido de reflex.db..."
        
        # Contar registros en reflex.db
        REFLEX_CURSOS=$(python3 -c "
import sqlite3
try:
    conn = sqlite3.connect('reflex.db')
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM curso')
    count = cursor.fetchone()[0]
    conn.close()
    print(count)
except:
    print('0')
" 2>/dev/null)
        
        echo "📈 Cursos en reflex.db: $REFLEX_CURSOS"
        
        # Si reflex.db está vacía, copiar desde data/saltoestudia.db
        if [ "$REFLEX_CURSOS" -eq "0" ]; then
            echo "🔄 reflex.db está vacía, copiando datos desde data/saltoestudia.db..."
            cp data/saltoestudia.db reflex.db
            echo "✅ Base de datos sincronizada"
        else
            echo "✅ reflex.db ya tiene datos, no es necesario sincronizar"
        fi
    else
        echo "🔄 reflex.db no existe, copiando desde data/saltoestudia.db..."
        cp data/saltoestudia.db reflex.db
        echo "✅ Base de datos creada y sincronizada"
    fi
else
    echo "⚠️  No se encontró data/saltoestudia.db"
    echo "💡 Ejecutando migraciones y seed..."
    
    # Ejecutar migraciones si no existen
    if [ -d "alembic" ]; then
        echo "🔄 Aplicando migraciones con Alembic..."
        alembic upgrade head
    else
        echo "🔄 Inicializando base de datos con Reflex..."
        reflex db migrate
    fi
    
    # Ejecutar seed
    if [ -f "seed.py" ]; then
        echo "🌱 Ejecutando seed..."
        python3 seed.py
    fi
    
    # Verificar que se creó la base de datos
    if [ -f "data/saltoestudia.db" ]; then
        echo "✅ Base de datos creada exitosamente"
        # Copiar a reflex.db para consistencia
        cp data/saltoestudia.db reflex.db
        echo "✅ Base de datos sincronizada"
    else
        echo "❌ Error: No se pudo crear la base de datos"
        exit 1
    fi
fi

# Verificación final
echo "🔍 Verificación final..."
CURSOS_FINAL=$(python3 -c "
import sqlite3
try:
    conn = sqlite3.connect('reflex.db')
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM curso')
    count = cursor.fetchone()[0]
    conn.close()
    print(count)
except:
    print('0')
" 2>/dev/null)

INSTITUCIONES_FINAL=$(python3 -c "
import sqlite3
try:
    conn = sqlite3.connect('reflex.db')
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM instituciones')
    count = cursor.fetchone()[0]
    conn.close()
    print(count)
except:
    print('0')
" 2>/dev/null)

echo "📊 Estado final de la base de datos:"
echo "   - Cursos: $CURSOS_FINAL"
echo "   - Instituciones: $INSTITUCIONES_FINAL"

if [ "$CURSOS_FINAL" -gt "0" ] && [ "$INSTITUCIONES_FINAL" -gt "0" ]; then
    echo "✅ Base de datos sincronizada correctamente"
    exit 0
else
    echo "❌ Error: La base de datos no tiene datos válidos"
    exit 1
fi 