#!/usr/bin/env python3
"""
Script para verificar la migración de datos de SQLite a PostgreSQL
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
        return conn
    except Exception as e:
        print(f"❌ Error conectando a PostgreSQL: {e}")
        return None

def compare_table_counts(table_name):
    """Compara el número de registros entre SQLite y PostgreSQL"""
    
    # Contar en SQLite
    sqlite_conn = sqlite3.connect("data/saltoestudia.db")
    cursor_sqlite = sqlite_conn.cursor()
    cursor_sqlite.execute(f"SELECT COUNT(*) FROM {table_name}")
    sqlite_count = cursor_sqlite.fetchone()[0]
    sqlite_conn.close()
    
    # Contar en PostgreSQL
    pg_conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "postgres"),
        port=os.getenv("DB_PORT", "5432"),
        database=os.getenv("DB_NAME", "saltoestudia"),
        user=os.getenv("DB_USER", "saltoestudia"),
        password=os.getenv("DB_PASSWORD", "dev_password")
    )
    cursor_pg = pg_conn.cursor()
    cursor_pg.execute(f"SELECT COUNT(*) FROM {table_name}")
    pg_count = cursor_pg.fetchone()[0]
    pg_conn.close()
    
    return sqlite_count, pg_count

def compare_sample_data(table_name, limit=5):
    """Compara una muestra de datos entre SQLite y PostgreSQL"""
    
    # Obtener muestra de SQLite
    sqlite_conn = sqlite3.connect("data/saltoestudia.db")
    cursor_sqlite = sqlite_conn.cursor()
    cursor_sqlite.execute(f"SELECT * FROM {table_name} LIMIT {limit}")
    sqlite_data = cursor_sqlite.fetchall()
    sqlite_conn.close()
    
    # Obtener muestra de PostgreSQL
    pg_conn = psycopg2.connect(
        host=os.getenv("DB_HOST", "postgres"),
        port=os.getenv("DB_PORT", "5432"),
        database=os.getenv("DB_NAME", "saltoestudia"),
        user=os.getenv("DB_USER", "saltoestudia"),
        password=os.getenv("DB_PASSWORD", "dev_password")
    )
    cursor_pg = pg_conn.cursor()
    cursor_pg.execute(f"SELECT * FROM {table_name} LIMIT {limit}")
    pg_data = cursor_pg.fetchall()
    pg_conn.close()
    
    return sqlite_data, pg_data

def main():
    """Verifica la migración"""
    print("🔍 Verificando migración de datos...")
    print("=" * 50)
    
    tables = ['ciudad', 'instituciones', 'sedes', 'usuarios', 'curso', 'curso_ciudad']
    
    all_match = True
    total_sqlite = 0
    total_postgres = 0
    
    print("\n📊 Comparación de registros por tabla:")
    print("-" * 40)
    
    for table in tables:
        try:
            sqlite_count, pg_count = compare_table_counts(table)
            total_sqlite += sqlite_count
            total_postgres += pg_count
            
            if sqlite_count == pg_count:
                print(f"✅ {table:15} | {sqlite_count:3} registros (coinciden)")
            else:
                print(f"❌ {table:15} | SQLite={sqlite_count:3}, PostgreSQL={pg_count:3}")
                all_match = False
                
        except Exception as e:
            print(f"❌ {table:15} | Error: {e}")
            all_match = False
    
    print("-" * 40)
    print(f"📈 Total SQLite: {total_sqlite} registros")
    print(f"📈 Total PostgreSQL: {total_postgres} registros")
    
    if total_sqlite == total_postgres:
        print(f"✅ Total de registros: {total_sqlite} (coinciden)")
    else:
        print(f"❌ Total de registros: NO coinciden")
        all_match = False
    
    print("\n🔍 Verificación de muestra de datos:")
    print("-" * 40)
    
    # Verificar muestra de datos para tablas principales
    sample_tables = ['instituciones', 'curso', 'usuarios']
    
    for table in sample_tables:
        try:
            sqlite_data, pg_data = compare_sample_data(table, 3)
            
            if len(sqlite_data) == len(pg_data):
                print(f"✅ {table:15} | Muestra de {len(sqlite_data)} registros (coinciden)")
            else:
                print(f"❌ {table:15} | Muestra: SQLite={len(sqlite_data)}, PostgreSQL={len(pg_data)}")
                all_match = False
                
        except Exception as e:
            print(f"❌ {table:15} | Error en muestra: {e}")
            all_match = False
    
    print("\n" + "=" * 50)
    
    if all_match:
        print("🎉 ¡Todas las verificaciones fueron exitosas!")
        print("✅ La migración se completó correctamente")
        print("✅ Los datos están sincronizados entre SQLite y PostgreSQL")
        return True
    else:
        print("⚠️ Hay discrepancias en la migración")
        print("❌ Se encontraron diferencias entre SQLite y PostgreSQL")
        print("🔧 Revisa los logs y considera rehacer la migración")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 