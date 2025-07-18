# ⚙️ Configuración del Sistema - Salto Estudia

## 📋 Resumen

Este documento describe todos los archivos de configuración del proyecto Salto Estudia, incluyendo variables de entorno, archivos Docker, configuración de Reflex y otros archivos de configuración importantes.

## 🔧 Archivos de Configuración Principales

### 1. `.env` - Variables de Entorno

**Propósito**: Configuración de variables de entorno para diferentes entornos.

**Ubicación**: `./.env` (local) y `/srv/docker/saltoestudia/.env` (VPS)

**Configuración de Desarrollo (Local)**:
```bash
# CONFIGURACIÓN DE ENTORNO - SALTO ESTUDIA (DESARROLLO)
# ========================================

# === BASE DE DATOS SQLITE ===
DATABASE_URL=sqlite:///data/saltoestudia.db
REFLEX_DB_URL=sqlite:///reflex.db

# === CONTRASEÑAS INDIVIDUALES DE USUARIOS ADMINISTRADORES ===
DEFAULT_SEED_PASSWORD=SaltoEstudia2024_Default!
CENUR_PASSWORD=Cenur_Segura_2024!
IAE_PASSWORD=IAE_Admin_2024!
CATALINA_PASSWORD=Catalina_Tech_2024!
ADMINISTRACION_PASSWORD=Admin_Escuela_2024!
AGRARIA_PASSWORD=Agraria_Campo_2024!
```

**Configuración de Producción (VPS)**:
```bash
# CONFIGURACIÓN DE ENTORNO - SALTO ESTUDIA (PRODUCCIÓN)
# ========================================

# === BASE DE DATOS POSTGRESQL ===
DATABASE_URL=postgresql://saltoestudia:SaltoEstudia2024_Postgres!@postgres:5432/saltoestudia
REFLEX_DB_URL=postgresql://saltoestudia:SaltoEstudia2024_Postgres!@postgres:5432/saltoestudia
DB_PASSWORD=SaltoEstudia2024_Postgres!

# === CONTRASEÑAS INDIVIDUALES DE USUARIOS ADMINISTRADORES ===
DEFAULT_SEED_PASSWORD=SaltoEstudia2024_Default!
CENUR_PASSWORD=Cenur_Segura_2024!
IAE_PASSWORD=IAE_Admin_2024!
CATALINA_PASSWORD=Catalina_Tech_2024!
ADMINISTRACION_PASSWORD=Admin_Escuela_2024!
AGRARIA_PASSWORD=Agraria_Campo_2024!

# === CONFIGURACIÓN DE PRODUCCIÓN ===
REFLEX_ENV=production
```

**⚠️ IMPORTANTE**: 
- El archivo `.env` **NO se sube a GitHub** por seguridad
- Para producción, **SIEMPRE** verificar que el archivo `.env` en el VPS tenga la configuración correcta de PostgreSQL
- Si PostgreSQL no se inicializa, verificar que `DB_PASSWORD` esté configurado

**Para actualizar .env en producción**:
```bash
# Opción 1: Crear archivo local y subirlo
scp env.production ubuntu@150.230.30.198:/srv/docker/saltoestudia/.env

# Opción 2: Editar directamente en el VPS
ssh ubuntu@150.230.30.198
cd /srv/docker/saltoestudia
nano .env
```

### 2. `rxconfig.py` - Configuración de Reflex

**Propósito**: Configuración global de la aplicación Reflex.

**Ubicación**: `./rxconfig.py`

**Configuración Principal**:
```python
import reflex as rx

config = rx.Config(
    app_name="saltoestudia",
    db_url="sqlite:///./data/saltoestudia.db",
    env=rx.Env.DEV,
    frontend_port=3000,
    backend_port=8000,
    api_url="http://localhost:8000",
    deploy_url="https://saltoestudia.infra.com.uy",
    tailwind={},
    bun_path="/usr/local/bin/bun",
)
```

**Parámetros Importantes**:
- **`app_name`**: Nombre de la aplicación
- **`db_url`**: URL de la base de datos SQLite
- **`env`**: Entorno (DEV/PROD)
- **`frontend_port`**: Puerto del frontend (3000)
- **`backend_port`**: Puerto del backend (8000)
- **`api_url`**: URL de la API en desarrollo
- **`deploy_url`**: URL de producción
- **`bun_path`**: Ruta al ejecutable de Bun

**Configuración por Entorno**:
```python
# Desarrollo
config = rx.Config(
    env=rx.Env.DEV,
    api_url="http://localhost:8000",
)

# Producción
config = rx.Config(
    env=rx.Env.PROD,
    api_url="https://saltoestudia.infra.com.uy",
)
```

---

### 2. `requirements.txt` - Dependencias de Python

**Propósito**: Lista de dependencias de Python necesarias para el proyecto.

**Ubicación**: `./requirements.txt`

**Dependencias Principales**:
```
reflex>=0.3.0
sqlmodel>=0.0.8
bcrypt>=4.0.1
alembic>=1.12.0
```

**Descripción de Dependencias**:
- **`reflex`**: Framework web para Python
- **`sqlmodel`**: ORM moderno para SQL
- **`bcrypt`**: Encriptación de contraseñas
- **`alembic`**: Migraciones de base de datos

**Instalación**:
```bash
pip install -r requirements.txt
```

---

### 3. `package.json` - Configuración de Node.js

**Propósito**: Configuración de dependencias y scripts de Node.js.

**Ubicación**: `./package.json`

**Contenido Principal**:
```json
{
  "name": "saltoestudia",
  "version": "1.0.0",
  "description": "Plataforma educativa para Salto, Uruguay",
  "scripts": {
    "dev": "docker compose -f docker-compose.desarrollo.yml up -d --build",
    "build": "docker compose -f docker-compose.production.yml build",
    "deploy": "./deploy-to-vps.sh"
  },
  "dependencies": {
    "bun": "latest"
  }
}
```

**Scripts Disponibles**:
- **`dev`**: Inicia en modo desarrollo con Docker
- **`build`**: Construye imagen de producción
- **`deploy`**: Despliega en VPS usando script automatizado

---

## 🐳 Configuración Docker

### 4. `docker-compose.yml` - Configuración Principal

**Propósito**: Configuración de contenedores para producción.

**Ubicación**: `./docker-compose.yml`

**Servicios Configurados**:
```yaml
version: '3.8'

services:
  app:
    build: .
    container_name: saltoestudia-app
    ports:
      - "3000:3000"  # Frontend
      - "8000:8000"  # Backend
    volumes:
      - ./data:/app/data  # Persistencia de BD
      - ./assets:/app/assets  # Assets estáticos
    environment:
      - DATABASE_URL=sqlite:///./data/saltoestudia.db
      - REFLEX_DB_URL=sqlite:///reflex.db
      - PYTHONPATH=/app
    networks:
      - traefik-net
    restart: unless-stopped

networks:
  traefik-net:
    external: true
```

**Configuración de Redes**:
- **`traefik-net`**: Red externa para Traefik
- **Puertos**: 3000 (frontend), 8000 (backend)
- **Volúmenes**: Persistencia de datos y assets

---

### 5. `docker-compose.desarrollo.yml` - Configuración de Desarrollo

**Propósito**: Configuración específica para desarrollo local.

**Ubicación**: `./docker-compose.desarrollo.yml`

**Diferencias con Producción**:
```yaml
services:
  app:
    build: 
      context: .
      dockerfile: dockerfile
    volumes:
      - .:/app  # Montaje completo para hot reload
      - ./data:/app/data
    environment:
      - REFLEX_ENV=development
      - DEBUG=true
    command: reflex run --backend-host 0.0.0.0 --backend-port 8000 --frontend-port 3000
```

**Características de Desarrollo**:
- **Hot reload**: Montaje completo del código
- **Debug**: Variables de entorno para desarrollo
- **Comando personalizado**: Reflex en modo desarrollo

---

### 6. `dockerfile` - Imagen de Desarrollo

**Propósito**: Definición de la imagen Docker para desarrollo.

**Ubicación**: `./dockerfile`

**Configuración**:
```dockerfile
FROM python:3.11-slim

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Instalar Bun
RUN curl -fsSL https://bun.sh/install | bash
ENV PATH="/root/.bun/bin:$PATH"

# Directorio de trabajo
WORKDIR /app

# Copiar archivos de dependencias
COPY requirements.txt package.json ./

# Instalar dependencias
RUN pip install -r requirements.txt
RUN bun install

# Copiar código fuente
COPY . .

# Exponer puertos
EXPOSE 3000 8000

# Comando por defecto
CMD ["reflex", "run", "--backend-host", "0.0.0.0", "--backend-port", "8000", "--frontend-port", "3000"]
```

**Características**:
- **Base**: Python 3.11 slim
- **Bun**: Para gestión de dependencias frontend
- **Puertos**: 3000 y 8000 expuestos
- **Hot reload**: Configurado para desarrollo

---

### 7. `dockerfile.production` - Imagen de Producción

**Propósito**: Definición de la imagen Docker optimizada para producción.

**Ubicación**: `./dockerfile.production`

**Optimizaciones de Producción**:
```dockerfile
FROM python:3.11-slim

# Instalar dependencias mínimas
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Instalar Bun
RUN curl -fsSL https://bun.sh/install | bash
ENV PATH="/root/.bun/bin:$PATH"

# Usuario no-root
RUN useradd -m -u 1000 appuser
USER appuser

WORKDIR /app

# Copiar solo archivos necesarios
COPY --chown=appuser:appuser requirements.txt package.json ./

# Instalar dependencias
RUN pip install --user -r requirements.txt
RUN bun install

# Copiar código fuente
COPY --chown=appuser:appuser . .

# Configuración de producción
ENV REFLEX_ENV=production
ENV PYTHONPATH=/app

EXPOSE 3000 8000

CMD ["reflex", "run", "--backend-host", "0.0.0.0", "--backend-port", "8000", "--frontend-port", "3000"]
```

**Seguridad de Producción**:
- **Usuario no-root**: Ejecuta como `appuser`
- **Dependencias mínimas**: Solo lo necesario
- **Permisos**: Archivos con propietario correcto

---

### 8. `.dockerignore` - Archivos Ignorados

**Propósito**: Define qué archivos ignorar al construir la imagen Docker.

**Ubicación**: `./.dockerignore`

**Contenido**:
```
.git
.gitignore
README.md
*.log
.env
data/
__pycache__/
.web/
```

**Archivos Ignorados**:
- **`.git`**: Repositorio Git
- **`*.log`**: Archivos de log
- **`.env`**: Variables de entorno
- **`data/`**: Base de datos local
- **`__pycache__/`**: Cache de Python
- **`.web/`**: Archivos temporales de Reflex

---

## 🔐 Variables de Entorno

### 9. `config-desarrollo.env` - Variables de Desarrollo

**Propósito**: Variables de entorno para desarrollo local.

**Ubicación**: `./config-desarrollo.env`

**Variables Principales**:
```bash
# Base de datos
DATABASE_URL=sqlite:///./data/saltoestudia.db
REFLEX_DB_URL=sqlite:///reflex.db

# Entorno
REFLEX_ENV=development
DEBUG=true

# Autenticación (datos de ejemplo)
CENUR_PASSWORD=password123
UTU_PASSWORD=password123
UTEC_PASSWORD=password123
UCU_PASSWORD=password123
UDELAR_PASSWORD=password123
CENUR_SALTO_PASSWORD=password123

# Configuración de la aplicación
PYTHONPATH=/app
FRONTEND_PORT=3000
BACKEND_PORT=8000
```

**Uso en Desarrollo**:
```bash
# Cargar variables
source config-desarrollo.env

# O usar con docker-compose
docker-compose --env-file config-desarrollo.env up
```

---

### 10. `.env` - Variables de Producción

**Propósito**: Variables de entorno para producción (NO en Git).

**Ubicación**: `./.env`

**⚠️ IMPORTANTE**: Este archivo NO debe estar en el repositorio Git.

**Variables de Producción**:
```bash
# Base de datos
DATABASE_URL=sqlite:///./data/saltoestudia.db
REFLEX_DB_URL=sqlite:///reflex.db

# Entorno
REFLEX_ENV=production
DEBUG=false

# Autenticación (contraseñas reales)
CENUR_PASSWORD=contraseña_segura_real
UTU_PASSWORD=contraseña_segura_real
UTEC_PASSWORD=contraseña_segura_real
UCU_PASSWORD=contraseña_segura_real
UDELAR_PASSWORD=contraseña_segura_real
CENUR_SALTO_PASSWORD=contraseña_segura_real

# Configuración de la aplicación
PYTHONPATH=/app
FRONTEND_PORT=3000
BACKEND_PORT=8000

# Configuración de VPS
VPS_HOST=150.230.30.198
VPS_USER=ubuntu
VPS_PATH=/home/ubuntu/saltoestudia
```

**Seguridad**:
- **Contraseñas reales**: No usar contraseñas de ejemplo
- **Archivo privado**: Nunca commitear en Git
- **Backup seguro**: Mantener backup en lugar seguro

---

## 🗄️ Configuración de Base de Datos

### 11. `alembic.ini` - Configuración de Migraciones

**Propósito**: Configuración de Alembic para migraciones de base de datos.

**Ubicación**: `./alembic.ini`

**Configuración Principal**:
```ini
[alembic]
script_location = alembic
sqlalchemy.url = sqlite:///./data/saltoestudia.db

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
```

**Configuración de Migraciones**:
- **`script_location`**: Directorio de migraciones
- **`sqlalchemy.url`**: URL de la base de datos
- **Logging**: Configuración de logs detallada

---

### 12. `alembic/env.py` - Entorno de Migraciones

**Propósito**: Configuración del entorno de migraciones de Alembic.

**Ubicación**: `./alembic/env.py`

**Configuración Principal**:
```python
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from saltoestudia.models import Base

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

**Funcionalidades**:
- **Metadatos**: Configuración de modelos SQLModel
- **Modo offline**: Para migraciones sin conexión
- **Modo online**: Para migraciones con conexión activa

---

## 🔧 Configuración de Scripts

### 13. `scripts/README.md` - Documentación de Scripts

**Propósito**: Documentación específica de los scripts de automatización.

**Ubicación**: `./scripts/README.md`

**Contenido**:
- Descripción de cada script
- Ejemplos de uso
- Parámetros disponibles
- Casos de uso comunes
- Solución de problemas

---

## 📁 Estructura de Configuración

### Organización de Archivos
```
saltoestudia/
├── rxconfig.py                    # Configuración Reflex
├── requirements.txt               # Dependencias Python
├── package.json                   # Configuración Node.js
├── docker-compose.yml             # Docker producción
├── docker-compose.desarrollo.yml  # Docker desarrollo
├── dockerfile                     # Imagen desarrollo
├── dockerfile.production          # Imagen producción
├── .dockerignore                  # Archivos ignorados
├── config-desarrollo.env          # Variables desarrollo
├── .env                           # Variables producción (NO en Git)
├── alembic.ini                    # Configuración migraciones
├── alembic/
│   └── env.py                     # Entorno migraciones
└── scripts/
    └── README.md                  # Documentación scripts
```

### Jerarquía de Configuración
1. **Variables de entorno**: Prioridad más alta
2. **Archivos de configuración**: Configuración por defecto
3. **Configuración de Reflex**: Configuración de la aplicación
4. **Configuración Docker**: Configuración de contenedores

---

## 🔄 Gestión de Configuraciones

### Cambio de Entorno

#### Desarrollo a Producción
```bash
# 1. Configurar entorno
./scripts/setup-env.sh produccion

# 2. Verificar configuración
./scripts/verify-production-setup.sh

# 3. Iniciar aplicación
./scripts/start-project.sh production
```

#### Producción a Desarrollo
```bash
# 1. Configurar entorno
./scripts/setup-env.sh desarrollo

# 2. Verificar configuración
./scripts/verify-setup.sh

# 3. Iniciar aplicación
./scripts/start-project.sh docker
```

### Backup de Configuración
```bash
# Crear backup
cp .env .env.backup.$(date +%Y%m%d_%H%M%S)

# Restaurar backup
cp .env.backup.20240115_143022 .env
```

---

## 🛡️ Seguridad de Configuración

### Buenas Prácticas

#### Variables de Entorno
- **Nunca** commitear archivos `.env` con credenciales reales
- **Usar** archivos de ejemplo para documentación
- **Validar** variables antes de usar
- **Rotar** contraseñas regularmente

#### Configuración Docker
- **Usuario no-root**: Ejecutar como usuario no privilegiado
- **Volúmenes**: Montar solo directorios necesarios
- **Redes**: Usar redes aisladas
- **Secrets**: Usar Docker secrets para credenciales

#### Configuración de Base de Datos
- **Backup**: Backup regular de la base de datos
- **Migraciones**: Usar Alembic para cambios de esquema
- **Validación**: Validar esquema antes de producción
- **Monitoreo**: Monitorear performance de queries

---

## 🔍 Verificación de Configuración

### Scripts de Verificación

#### Verificación Completa
```bash
./scripts/verify-setup.sh
```

#### Verificación de Producción
```bash
./scripts/verify-production-setup.sh
```

#### Verificación de Seguridad
```bash
./scripts/security_check.sh
```

### Verificaciones Manuales

#### Variables de Entorno
```bash
# Verificar variables cargadas
env | grep -E "(DATABASE|REFLEX|PYTHON)"

# Verificar archivo .env
ls -la .env
```

#### Configuración Docker
```bash
# Verificar contenedores
docker ps

# Verificar redes
docker network ls

# Verificar volúmenes
docker volume ls
```

#### Configuración de Base de Datos
```bash
# Verificar conexión
python -c "from saltoestudia.database import engine; print('OK')"

# Verificar migraciones
alembic current
alembic history
```

---

## 📚 Referencias

### Documentación Relacionada
- **`SCRIPTS.md`**: Documentación de scripts
- **`DEPLOYMENT.md`**: Guía de despliegue
- **`ENTORNOS.md`**: Configuración de entornos
- **`TROUBLESHOOTING.md`**: Solución de problemas

### Comandos Útiles
```bash
# Ver configuración actual
cat rxconfig.py

# Ver variables de entorno
cat config-desarrollo.env

# Ver configuración Docker
docker-compose config

# Ver migraciones
alembic history --verbose
```

---

*Esta documentación se actualiza automáticamente con cada cambio en la configuración del sistema.* 