#!/bin/bash
set -e

echo "🚀 SALTO ESTUDIA - SCRIPT DE INICIO (Reflex 0.6.4 + AG Grid)"
echo "============================================================"

# Nos aseguramos de estar en el directorio correcto
cd /app

# --- 1. Verificar/Inicializar Reflex 0.6.4 ---
echo "⚙️  Verificando inicialización de Reflex 0.6.4..."
if [ ! -d ".web" ] || [ ! -d ".states" ]; then
    echo "   -> Inicializando Reflex 0.6.4..."
    reflex init --loglevel info || true
    echo "✅ Reflex 0.6.4 inicializado."
else
    echo "✅ Reflex ya está inicializado."
fi

# --- 2. Preparar directorios necesarios ---
echo "📁 Preparando directorios necesarios..."
mkdir -p /app/.web /app/.states /app/data
chmod -R 755 /app/.web /app/.states
echo "✅ Directorios preparados."

# --- 3. Verificación de Base de Datos SQLite ---
echo "🗄️  Verificando configuración de base de datos SQLite..."
mkdir -p /app/data
echo "✅ Base de datos SQLite configurada correctamente."

# --- 4. Creación de Tablas con SQLModel ---
echo "🗄️  Creando/verificando tablas de la base de datos con rx.Model.create_all()..."
python -c "
import os
import sys
sys.path.append('/app')

try:
    from saltoestudia.database import engine
    from saltoestudia.models import Institucion, Curso, Usuario
    
    print('Intentando crear todas las tablas si no existen...')
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(engine)
    print('✅ Tablas verificadas/creadas correctamente.')
except Exception as e:
    print(f'❌ Error al crear tablas: {e}')
    exit(1)
"

# --- 5. Poblar la Base de Datos con el Seed ---
echo "🌱 Poblando la base de datos con datos iniciales (seed)..."
python seed.py
echo "✅ Seed completado exitosamente."

# --- 6. Iniciar la aplicación Reflex 0.6.4 con AG Grid ---
echo "🚀 Iniciando la aplicación Reflex 0.6.4 con AG Grid..."
echo "   -> Frontend: http://localhost:3000"
echo "   -> Backend:  http://localhost:8000"
echo "   -> AG Grid:  ✅ Implementado en /cursos y /admin"

# Ejecutar Reflex con la configuración correcta
exec reflex run --host 0.0.0.0 --port 3000 --backend-host 0.0.0.0 --backend-port 8000

echo "✅ Aplicación iniciada con AG Grid funcionando." 