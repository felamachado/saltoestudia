# 📊 Datos y Migraciones - Salto Estudia

## 📋 Resumen

Este documento describe todos los archivos relacionados con datos del proyecto Salto Estudia, incluyendo migraciones de base de datos, scripts de seed, inicialización y gestión de datos.

## 🗄️ Base de Datos

### 1. `data/` - Directorio de Datos

**Propósito**: Almacena la base de datos SQLite y archivos de datos persistentes.

**Ubicación**: `./data/`

**Contenido**:
```
data/
├── saltoestudia.db          # Base de datos principal
├── reflex.db                # Base de datos de Reflex
└── backups/                 # Backups automáticos
    ├── saltoestudia_20240115.db
    └── saltoestudia_20240114.db
```

**Configuración**:
- **Base de datos principal**: `saltoestudia.db`
- **Base de datos Reflex**: `reflex.db`
- **Backups**: Automáticos diarios
- **Permisos**: 666 para escritura

---

### 2. `init_db.py` - Inicialización de Base de Datos

**Propósito**: Crea la estructura inicial de la base de datos.

**Ubicación**: `./init_db.py`

**Funcionalidades**:
```python
from sqlmodel import SQLModel, create_engine
from saltoestudia.models import *
import os

def init_database():
    """Inicializa la base de datos con todas las tablas."""
    database_url = os.getenv("DATABASE_URL", "sqlite:///./data/saltoestudia.db")
    engine = create_engine(database_url, echo=False)
    
    # Crear todas las tablas
    SQLModel.metadata.create_all(engine)
    
    print("✅ Base de datos inicializada correctamente")

if __name__ == "__main__":
    init_database()
```

**Uso**:
```bash
# Inicializar base de datos
python init_db.py

# Con variables de entorno específicas
DATABASE_URL=sqlite:///./data/test.db python init_db.py
```

**Tablas Creadas**:
- **`usuario`**: Usuarios del sistema
- **`institucion`**: Instituciones educativas
- **`sede`**: Sedes de las instituciones
- **`curso`**: Cursos ofrecidos
- **`curso_ciudad`**: Relación cursos-ciudades

---

## 🌱 Scripts de Seed

### 3. `seed.py` - Datos de Ejemplo

**Propósito**: Carga datos de ejemplo en la base de datos.

**Ubicación**: `./seed.py`

**Datos Incluidos**:

#### Instituciones Educativas
```python
instituciones = [
    {
        "nombre": "CENUR Litoral Norte",
        "descripcion": "Centro Universitario Regional del Litoral Norte",
        "web": "https://www.cenur.edu.uy",
        "logo": "logo-cenur.png"
    },
    {
        "nombre": "UTU",
        "descripcion": "Universidad del Trabajo del Uruguay",
        "web": "https://www.utu.edu.uy",
        "logo": "logoutu.png"
    },
    # ... más instituciones
]
```

#### Cursos de Ejemplo
```python
cursos = [
    {
        "nombre": "Tecnicatura en Informática",
        "nivel": "Técnico",
        "duracion_numero": 3,
        "duracion_unidad": "años",
        "requisitos_ingreso": "Bachillerato completo",
        "lugar": "Salto",
        "informacion": "Formación en desarrollo de software",
        "institucion_id": 1,
        "ciudades": ["Salto", "Paysandú"]
    },
    # ... más cursos
]
```

#### Usuarios Administradores
```python
usuarios = [
    {
        "correo": "admin@cenur.edu.uy",
        "password": "password123",  # Se hashea con bcrypt
        "institucion_id": 1
    },
    # ... más usuarios
]
```

**Funcionalidades**:
- **Hash de contraseñas**: Usa bcrypt para seguridad
- **Relaciones**: Crea relaciones entre entidades
- **Validación**: Valida datos antes de insertar
- **Rollback**: Maneja errores con rollback

**Uso**:
```bash
# Cargar datos de ejemplo
python seed.py

# Con base de datos específica
DATABASE_URL=sqlite:///./data/test.db python seed.py
```

---

## 🔄 Migraciones de Base de Datos

### 4. `alembic/` - Sistema de Migraciones

**Propósito**: Gestión de cambios en el esquema de la base de datos.

**Ubicación**: `./alembic/`

**Estructura**:
```
alembic/
├── env.py                    # Configuración del entorno
├── README                    # Documentación
├── script.py.mako           # Plantilla de migraciones
└── versions/                # Archivos de migración
    ├── 20e1d6c0be67_.py     # Migración inicial
    ├── 35434a546307_create_all_tables.py
    ├── b9ff636d97ad_.py
    ├── cd9ff636d97ad_.py
    └── f220f758945e_.py
```

---

### 5. `alembic/env.py` - Entorno de Migraciones

**Propósito**: Configuración del entorno de migraciones.

**Ubicación**: `./alembic/env.py`

**Configuración Principal**:
```python
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from saltoestudia.models import Base

# Configuración de metadatos
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Ejecuta migraciones en modo offline."""
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
    """Ejecuta migraciones en modo online."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, 
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()
```

---

### 6. Migraciones Específicas

#### Migración Inicial: `20e1d6c0be67_.py`
**Propósito**: Crea la estructura inicial de la base de datos.

**Contenido**:
```python
"""Initial migration

Revision ID: 20e1d6c0be67
Revises: 
Create Date: 2024-01-15 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

def upgrade() -> None:
    # Crear tabla usuario
    op.create_table('usuario',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('correo', sa.String(), nullable=False),
        sa.Column('password_hash', sa.String(), nullable=False),
        sa.Column('institucion_id', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('correo')
    )
    
    # Crear tabla institucion
    op.create_table('institucion',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nombre', sa.String(), nullable=False),
        sa.Column('descripcion', sa.Text(), nullable=True),
        sa.Column('web', sa.String(), nullable=True),
        sa.Column('logo', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    # ... más tablas
```

#### Migración de Tablas: `35434a546307_create_all_tables.py`
**Propósito**: Crea todas las tablas del sistema.

**Contenido**:
```python
"""Create all tables

Revision ID: 35434a546307
Revises: 20e1d6c0be67
Create Date: 2024-01-15 11:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

def upgrade() -> None:
    # Crear tabla sede
    op.create_table('sede',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nombre', sa.String(), nullable=False),
        sa.Column('direccion', sa.String(), nullable=True),
        sa.Column('telefono', sa.String(), nullable=True),
        sa.Column('email', sa.String(), nullable=True),
        sa.Column('web', sa.String(), nullable=True),
        sa.Column('ciudad', sa.String(), nullable=False),
        sa.Column('institucion_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['institucion_id'], ['institucion.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Crear tabla curso
    op.create_table('curso',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nombre', sa.String(), nullable=False),
        sa.Column('nivel', sa.String(), nullable=False),
        sa.Column('duracion_numero', sa.Integer(), nullable=False),
        sa.Column('duracion_unidad', sa.String(), nullable=False),
        sa.Column('requisitos_ingreso', sa.Text(), nullable=True),
        sa.Column('lugar', sa.String(), nullable=False),
        sa.Column('informacion', sa.Text(), nullable=True),
        sa.Column('institucion_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['institucion_id'], ['institucion.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Crear tabla curso_ciudad
    op.create_table('curso_ciudad',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('curso_id', sa.Integer(), nullable=False),
        sa.Column('ciudad', sa.String(), nullable=False),
        sa.ForeignKeyConstraint(['curso_id'], ['curso.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
```

---

## 📊 Gestión de Datos

### 7. Operaciones de Base de Datos

#### Lectura de Datos
```python
def obtener_cursos() -> List[Dict[str, Any]]:
    """Obtiene todos los cursos con información de institución."""
    with Session(engine) as session:
        query = (
            select(
                Curso.id,
                Curso.nombre,
                Curso.nivel,
                Curso.duracion_numero,
                Curso.duracion_unidad,
                Curso.requisitos_ingreso,
                Curso.lugar,
                Curso.informacion,
                Institucion.nombre.label("institucion_nombre"),
                Institucion.web.label("institucion_web"),
                Institucion.logo.label("institucion_logo")
            )
            .join(Institucion, Curso.institucion_id == Institucion.id)
        )
        
        results = session.exec(query).all()
        return [dict(row) for row in results]
```

#### Escritura de Datos
```python
def crear_curso(datos: Dict[str, Any]) -> Curso:
    """Crea un nuevo curso en la base de datos."""
    with Session(engine) as session:
        curso = Curso(**datos)
        session.add(curso)
        session.commit()
        session.refresh(curso)
        return curso
```

#### Actualización de Datos
```python
def actualizar_curso(curso_id: int, datos: Dict[str, Any]) -> Curso:
    """Actualiza un curso existente."""
    with Session(engine) as session:
        curso = session.get(Curso, curso_id)
        if not curso:
            raise ValueError(f"Curso {curso_id} no encontrado")
        
        for key, value in datos.items():
            setattr(curso, key, value)
        
        session.commit()
        session.refresh(curso)
        return curso
```

#### Eliminación de Datos
```python
def eliminar_curso(curso_id: int) -> bool:
    """Elimina un curso de la base de datos."""
    with Session(engine) as session:
        curso = session.get(Curso, curso_id)
        if not curso:
            return False
        
        session.delete(curso)
        session.commit()
        return True
```

---

## 🔄 Comandos de Migración

### Comandos Básicos

#### Ver Estado Actual
```bash
# Ver migración actual
alembic current

# Ver historial de migraciones
alembic history

# Ver migraciones pendientes
alembic heads
```

#### Crear Nueva Migración
```bash
# Crear migración automática
alembic revision --autogenerate -m "Descripción del cambio"

# Crear migración manual
alembic revision -m "Descripción del cambio"
```

#### Aplicar Migraciones
```bash
# Aplicar todas las migraciones pendientes
alembic upgrade head

# Aplicar hasta una migración específica
alembic upgrade 35434a546307

# Aplicar una migración hacia adelante
alembic upgrade +1
```

#### Revertir Migraciones
```bash
# Revertir una migración
alembic downgrade -1

# Revertir hasta una migración específica
alembic downgrade 20e1d6c0be67

# Revertir todas las migraciones
alembic downgrade base
```

---

## 🛡️ Backup y Recuperación

### 8. Sistema de Backup

#### Backup Automático
```bash
#!/bin/bash
# scripts/backup-db.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="./data/backups"
DB_FILE="./data/saltoestudia.db"

# Crear directorio de backup si no existe
mkdir -p $BACKUP_DIR

# Crear backup
cp $DB_FILE $BACKUP_DIR/saltoestudia_$DATE.db

# Comprimir backup
gzip $BACKUP_DIR/saltoestudia_$DATE.db

# Mantener solo los últimos 7 backups
ls -t $BACKUP_DIR/saltoestudia_*.db.gz | tail -n +8 | xargs -r rm

echo "Backup creado: saltoestudia_$DATE.db.gz"
```

#### Restauración de Backup
```bash
#!/bin/bash
# scripts/restore-db.sh

BACKUP_FILE=$1
DB_FILE="./data/saltoestudia.db"

if [ -z "$BACKUP_FILE" ]; then
    echo "Uso: $0 <archivo_backup>"
    exit 1
fi

# Detener aplicación
docker-compose down

# Crear backup del estado actual
cp $DB_FILE $DB_FILE.backup.$(date +%Y%m%d_%H%M%S)

# Restaurar backup
gunzip -c $BACKUP_FILE > $DB_FILE

# Reiniciar aplicación
docker-compose up -d

echo "Backup restaurado: $BACKUP_FILE"
```

---

## 📈 Monitoreo de Datos

### 9. Métricas de Base de Datos

#### Estadísticas Básicas
```python
def obtener_estadisticas() -> Dict[str, Any]:
    """Obtiene estadísticas de la base de datos."""
    with Session(engine) as session:
        total_usuarios = session.exec(select(func.count(Usuario.id))).first()
        total_instituciones = session.exec(select(func.count(Institucion.id))).first()
        total_cursos = session.exec(select(func.count(Curso.id))).first()
        total_sedes = session.exec(select(func.count(Sede.id))).first()
        
        return {
            "usuarios": total_usuarios,
            "instituciones": total_instituciones,
            "cursos": total_cursos,
            "sedes": total_sedes
        }
```

#### Logs de Operaciones
```python
def log_operacion(usuario_id: int, operacion: str, detalles: str):
    """Registra una operación en la base de datos."""
    with Session(engine) as session:
        log = LogOperacion(
            usuario_id=usuario_id,
            operacion=operacion,
            detalles=detalles,
            timestamp=datetime.now()
        )
        session.add(log)
        session.commit()
```

---

## 🔍 Verificación de Datos

### 10. Scripts de Verificación

#### Verificación de Integridad
```python
def verificar_integridad() -> List[str]:
    """Verifica la integridad de los datos."""
    errores = []
    
    with Session(engine) as session:
        # Verificar usuarios sin institución
        usuarios_sin_institucion = session.exec(
            select(Usuario).where(Usuario.institucion_id.is_(None))
        ).all()
        
        if usuarios_sin_institucion:
            errores.append(f"Usuarios sin institución: {len(usuarios_sin_institucion)}")
        
        # Verificar cursos sin institución
        cursos_sin_institucion = session.exec(
            select(Curso).where(Curso.institucion_id.is_(None))
        ).all()
        
        if cursos_sin_institucion:
            errores.append(f"Cursos sin institución: {len(cursos_sin_institucion)}")
        
        # Verificar sedes sin institución
        sedes_sin_institucion = session.exec(
            select(Sede).where(Sede.institucion_id.is_(None))
        ).all()
        
        if sedes_sin_institucion:
            errores.append(f"Sedes sin institución: {len(sedes_sin_institucion)}")
    
    return errores
```

#### Verificación de Consistencia
```python
def verificar_consistencia() -> Dict[str, Any]:
    """Verifica la consistencia de los datos."""
    with Session(engine) as session:
        # Verificar que todas las instituciones tengan al menos una sede
        instituciones_sin_sedes = session.exec(
            select(Institucion)
            .outerjoin(Sede)
            .where(Sede.id.is_(None))
        ).all()
        
        # Verificar que todos los cursos tengan al menos una ciudad
        cursos_sin_ciudades = session.exec(
            select(Curso)
            .outerjoin(CursoCiudad)
            .where(CursoCiudad.id.is_(None))
        ).all()
        
        return {
            "instituciones_sin_sedes": len(instituciones_sin_sedes),
            "cursos_sin_ciudades": len(cursos_sin_ciudades),
            "total_instituciones": session.exec(select(func.count(Institucion.id))).first(),
            "total_cursos": session.exec(select(func.count(Curso.id))).first()
        }
```

---

## 🚀 Optimización de Datos

### 11. Índices y Performance

#### Índices Recomendados
```sql
-- Índice en correo de usuario (único)
CREATE UNIQUE INDEX idx_usuario_correo ON usuario(correo);

-- Índice en institución_id para búsquedas
CREATE INDEX idx_curso_institucion ON curso(institucion_id);
CREATE INDEX idx_sede_institucion ON sede(institucion_id);
CREATE INDEX idx_usuario_institucion ON usuario(institucion_id);

-- Índice en ciudad para filtros
CREATE INDEX idx_sede_ciudad ON sede(ciudad);
CREATE INDEX idx_curso_ciudad_ciudad ON curso_ciudad(ciudad);

-- Índice en nivel para filtros
CREATE INDEX idx_curso_nivel ON curso(nivel);
```

#### Consultas Optimizadas
```python
def obtener_cursos_optimizado(filtros: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Obtiene cursos con filtros optimizados."""
    with Session(engine) as session:
        query = (
            select(
                Curso.id,
                Curso.nombre,
                Curso.nivel,
                Curso.duracion_numero,
                Curso.duracion_unidad,
                Curso.requisitos_ingreso,
                Curso.lugar,
                Curso.informacion,
                Institucion.nombre.label("institucion_nombre"),
                Institucion.web.label("institucion_web"),
                Institucion.logo.label("institucion_logo")
            )
            .join(Institucion, Curso.institucion_id == Institucion.id)
        )
        
        # Aplicar filtros
        if filtros.get("nivel"):
            query = query.where(Curso.nivel == filtros["nivel"])
        
        if filtros.get("institucion_id"):
            query = query.where(Curso.institucion_id == filtros["institucion_id"])
        
        if filtros.get("lugar"):
            query = query.where(Curso.lugar == filtros["lugar"])
        
        # Ordenar por nombre
        query = query.order_by(Curso.nombre)
        
        results = session.exec(query).all()
        return [dict(row) for row in results]
```

---

## 📚 Referencias

### Documentación Relacionada
- **`ARCHITECTURE.md`**: Arquitectura del sistema
- **`COMPONENTS.md`**: Componentes del sistema
- **`CONFIGURATION.md`**: Configuración del sistema
- **`DEPLOYMENT.md`**: Guía de despliegue

### Comandos Útiles
```bash
# Ver estado de migraciones
alembic current

# Crear nueva migración
alembic revision --autogenerate -m "Nuevo campo"

# Aplicar migraciones
alembic upgrade head

# Verificar base de datos
python -c "from saltoestudia.database import engine; print('OK')"

# Crear backup
./scripts/backup-db.sh

# Restaurar backup
./scripts/restore-db.sh backup_file.db.gz
```

---

*Esta documentación se actualiza automáticamente con cada cambio en los datos del sistema.* 