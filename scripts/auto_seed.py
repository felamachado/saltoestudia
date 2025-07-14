import sqlite3
import os
import subprocess

DB_PATH = os.getenv("DATABASE_URL", "sqlite:///./data/saltoestudia.db")
if DB_PATH.startswith("sqlite:///"):
    db_file = DB_PATH.replace("sqlite:///", "")
else:
    db_file = "data/saltoestudia.db"

# Quitar barra inicial si existe (por rutas absolutas)
if db_file.startswith("/") and not os.path.exists(db_file):
    db_file = db_file[1:]

if not os.path.exists(db_file):
    print(f"[auto_seed] La base de datos no existe: {db_file}")
    needs_seed = True
else:
    conn = sqlite3.connect(db_file)
    c = conn.cursor()
    try:
        c.execute('SELECT COUNT(*) FROM instituciones')
        instituciones = c.fetchone()[0]
        c.execute('SELECT COUNT(*) FROM cursos')
        cursos = c.fetchone()[0]
        needs_seed = (instituciones == 0 or cursos == 0)
    except Exception as e:
        print(f"[auto_seed] Error al consultar la base: {e}")
        needs_seed = True
    finally:
        conn.close()

if needs_seed:
    print("[auto_seed] Ejecutando seed.py para poblar la base de datos...")
    subprocess.run(["python3", "seed.py"]) 
else:
    print("[auto_seed] La base de datos ya tiene datos. No se ejecuta el seed.") 