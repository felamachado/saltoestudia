#!/usr/bin/env python3
"""
Script de migración de SQLite a PostgreSQL
Migra todos los datos de la base de datos SQLite a PostgreSQL
"""

import os
import sys
import sqlite3
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

def get_sqlite_connection():
    """Conecta a la base de datos SQLite"""
    sqlite_path = "data/saltoestudia.db"
    if not os.path.exists(sqlite_path):
        print(f"❌ No se encontró la base de datos SQLite en {sqlite_path}")
        return None
    
    try:
        conn = sqlite3.connect(sqlite_path)
        print(f"✅ Conectado a SQLite: {sqlite_path}")
        return conn
    except Exception as e:
        print(f"❌ Error conectando a SQLite: {e}")
        return None

def get_postgres_connection():
    """Conecta a PostgreSQL"""
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "postgres"),
            port=os.getenv("DB_PORT", "5432"),
            database=os.getenv("DB_NAME", "saltoestudia"),
            user=os.getenv("DB_USER", "saltoestudia"),
            password=os.getenv("DB_PASSWORD", "dev_password")
        )
        print(f"✅ Conectado a PostgreSQL: {os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}")
        return conn
    except Exception as e:
        print(f"❌ Error conectando a PostgreSQL: {e}")
        return None

def get_table_schema(sqlite_conn, table_name):
    """Obtiene el esquema de una tabla de SQLite"""
    cursor = sqlite_conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    
    schema = []
    for col in columns:
        schema.append({
            'name': col[1],
            'type': col[2],
            'notnull': col[3],
            'default': col[4],
            'pk': col[5]
        })
    
    return schema

def migrate_table(sqlite_conn, pg_conn, table_name):
    """Migra una tabla específica"""
    print(f"🔄 Migrando tabla: {table_name}")
    
    try:
        # Obtener datos de SQLite
        cursor_sqlite = sqlite_conn.cursor()
        cursor_sqlite.execute(f"SELECT * FROM {table_name}")
        rows = cursor_sqlite.fetchall()
        
        if not rows:
            print(f"   ⚠️ Tabla {table_name} está vacía")
            return True
        
        # Obtener nombres de columnas
        columns = [description[0] for description in cursor_sqlite.description]
        print(f"   📊 {len(rows)} registros encontrados")
        
        # Insertar en PostgreSQL
        cursor_pg = pg_conn.cursor()
        
        # Crear placeholders para la query
        placeholders = ','.join(['%s'] * len(columns))
        columns_str = ','.join(columns)
        
        query = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"
        
        # Ejecutar inserción
        cursor_pg.executemany(query, rows)
        pg_conn.commit()
        
        print(f"   ✅ {len(rows)} registros migrados exitosamente")
        return True
        
    except Exception as e:
        pg_conn.rollback()
        print(f"   ❌ Error migrando {table_name}: {e}")
        return False

def verify_table_migration(sqlite_conn, pg_conn, table_name):
    """Verifica que la migración de una tabla fue exitosa"""
    try:
        # Contar registros en SQLite
        cursor_sqlite = sqlite_conn.cursor()
        cursor_sqlite.execute(f"SELECT COUNT(*) FROM {table_name}")
        sqlite_count = cursor_sqlite.fetchone()[0]
        
        # Contar registros en PostgreSQL
        cursor_pg = pg_conn.cursor()
        cursor_pg.execute(f"SELECT COUNT(*) FROM {table_name}")
        pg_count = cursor_pg.fetchone()[0]
        
        if sqlite_count == pg_count:
            print(f"   ✅ Verificación {table_name}: {sqlite_count} registros (coinciden)")
            return True
        else:
            print(f"   ❌ Verificación {table_name}: SQLite={sqlite_count}, PostgreSQL={pg_count}")
            return False
            
    except Exception as e:
        print(f"   ❌ Error verificando {table_name}: {e}")
        return False

def main():
    """Función principal de migración"""
    print("🚀 Iniciando migración de SQLite a PostgreSQL...")
    print("=" * 50)
    
    # Conectar a SQLite
    sqlite_conn = get_sqlite_connection()
    if not sqlite_conn:
        return False
    
    # Conectar a PostgreSQL
    pg_conn = get_postgres_connection()
    if not pg_conn:
        sqlite_conn.close()
        return False
    
    # Tablas a migrar (en orden de dependencias)
    tables = [
        'ciudad',
        'instituciones', 
        'sedes',
        'usuarios',
        'curso',
        'curso_ciudad'
    ]
    
    print("\n📋 Tablas a migrar:")
    for table in tables:
        print(f"   - {table}")
    
    print("\n🔄 Iniciando migración...")
    print("-" * 30)
    
    migration_success = True
    verification_success = True
    
    try:
        # Migrar cada tabla
        for table in tables:
            success = migrate_table(sqlite_conn, pg_conn, table)
            if not success:
                migration_success = False
                break
        
        if migration_success:
            print("\n✅ Migración completada exitosamente")
            print("\n🔍 Verificando migración...")
            print("-" * 30)
            
            # Verificar cada tabla
            for table in tables:
                success = verify_table_migration(sqlite_conn, pg_conn, table)
                if not success:
                    verification_success = False
            
            if verification_success:
                print("\n🎉 ¡Migración y verificación completadas exitosamente!")
                print("\n📊 Resumen:")
                print(f"   - Tablas migradas: {len(tables)}")
                print(f"   - Estado: ✅ Exitoso")
                print(f"   - Base de datos: PostgreSQL activa")
            else:
                print("\n⚠️ Migración completada pero hay discrepancias en la verificación")
                return False
        else:
            print("\n❌ Error durante la migración")
            return False
            
    except Exception as e:
        print(f"\n❌ Error inesperado durante la migración: {e}")
        return False
    finally:
        sqlite_conn.close()
        pg_conn.close()
        print("\n🔒 Conexiones cerradas")
    
    return migration_success and verification_success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 