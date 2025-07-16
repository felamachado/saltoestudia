#!/usr/bin/env python3
"""
Script de inicialización de base de datos para Salto Estudia
Reemplaza la lógica de start.sh para crear tablas
"""

import os
import sys

# Agregar el directorio actual al path
sys.path.append('/app')

def init_database():
    """Inicializa las tablas de la base de datos"""
    try:
        print('🗄️ Importando módulos de la base de datos...')
        from saltoestudia.database import engine
        from saltoestudia.models import Institucion, Curso, Usuario
        
        print('📋 Creando todas las tablas si no existen...')
        from sqlmodel import SQLModel
        SQLModel.metadata.create_all(engine)
        
        print('✅ Tablas de la base de datos creadas correctamente.')
        return True
        
    except Exception as e:
        print(f'❌ Error al crear tablas de la base de datos: {e}')
        return False

if __name__ == "__main__":
    success = init_database()
    if not success:
        sys.exit(1)
    print('🎉 Inicialización de base de datos completada.') 