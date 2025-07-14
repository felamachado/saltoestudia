#!/bin/bash

# Script definitivo para desarrollo local de Salto Estudia
# Limpia puertos y arranca Reflex usando la base de datos correcta

set -e

# 1. Matar procesos que puedan estar usando los puertos
pkill -f reflex || true
pkill -f "bun run dev" || true
pkill -f "python3 -m http.server" || true
lsof -ti :3000 | xargs -r kill -9
lsof -ti :8000 | xargs -r kill -9

# 2. Verificar que el .env apunte a la base correcta
if ! grep -q 'DATABASE_URL=sqlite:////home/felipe/Escritorio/Proyectos/saltoestudia/data/saltoestudia.db' .env 2>/dev/null; then
  echo 'DATABASE_URL=sqlite:////home/felipe/Escritorio/Proyectos/saltoestudia/data/saltoestudia.db' > .env
  echo "[INFO] Se creó .env apuntando a la base de datos correcta."
fi

# 3. Solo migrar si la base no existe o está vacía
DB_FILE="data/saltoestudia.db"
MIGRAR=0
if [ ! -f "$DB_FILE" ]; then
  MIGRAR=1
else
  INSTITUCIONES=$(python3 -c "import sqlite3; c=sqlite3.connect('$DB_FILE').cursor(); c.execute('SELECT COUNT(*) FROM sqlite_master WHERE type=\'table\' AND name=\'instituciones\';'); print(c.fetchone()[0])")
  if [ "$INSTITUCIONES" = "0" ]; then
    MIGRAR=1
  fi
fi
if [ "$MIGRAR" = "1" ]; then
  echo "[INFO] Ejecutando migraciones de Reflex..."
  reflex db migrate || true
else
  echo "[INFO] Migraciones NO necesarias. La base ya tiene tablas."
fi

# 4. Poblar la base de datos si está vacía
python3 scripts/auto_seed.py

# 5. Arrancar Reflex
reflex run --backend-host 0.0.0.0 --backend-port 8000 --frontend-port 3000 