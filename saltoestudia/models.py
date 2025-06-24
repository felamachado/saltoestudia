# saltoestudia/models.py

# ================================================================================
# MODELOS DE BASE DE DATOS - SALTO ESTUDIA
# ================================================================================
# 
# Este archivo define la estructura de datos del sistema usando SQLModel,
# que combina SQLAlchemy (ORM) con Pydantic (validación).
#
# ARQUITECTURA DE DATOS:
# - Institucion: Entidad principal (universidades, institutos, escuelas)
# - Usuario: Administradores por institución para gestionar cursos
# - Curso: Oferta educativa de cada institución
#
# RELACIONES:
# - Institucion 1:N Usuario (una institución tiene muchos administradores)
# - Institucion 1:N Curso (una institución ofrece muchos cursos)
# - Usuario N:1 Institucion (cada admin pertenece a una institución)
# - Curso N:1 Institucion (cada curso pertenece a una institución)
#
# PATRON UTILIZADO:
# - SQLModel para definir tanto la tabla de BD como el modelo Pydantic
# - Relationships para navegación entre entidades relacionadas
# - Foreign keys para integridad referencial
# ================================================================================

from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship

# ================================================================================
# MODELO INSTITUCION - Entidad principal del sistema
# ================================================================================
class Institucion(SQLModel, table=True):
    """
    Representa una institución educativa en Salto, Uruguay.
    
    Esta es la entidad central del sistema. Cada institución puede tener:
    - Múltiples usuarios administradores
    - Múltiples cursos en su oferta educativa
    
    CAMPOS:
    - id: Clave primaria autoincremental
    - nombre: Nombre oficial de la institución (ej: "UDELAR – CENUR LN")
    - direccion: Dirección física para contacto
    - telefono: Número de contacto
    - email: Correo institucional
    - web: Sitio web oficial (opcional)
    - logo: Ruta al archivo de logo (ej: "/logos/logo-cenur.png")
    
    RELACIONES:
    - cursos: Lista de cursos que ofrece la institución
    - usuarios: Lista de administradores de la institución
    
    UTILIZADO EN:
    - pages/instituciones.py: Galería de instituciones
    - pages/cursos.py: Filtro por institución
    - pages/admin.py: Contexto del usuario logueado
    - state.py: Carga de datos para filtros y autenticación
    """
    __tablename__ = "instituciones"
    
    # === CAMPOS PRINCIPALES ===
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str                           # Nombre oficial de la institución
    direccion: Optional[str] = None       # Dirección física
    telefono: Optional[str] = None        # Teléfono de contacto
    email: Optional[str] = None           # Email institucional
    web: Optional[str] = None             # Sitio web oficial
    logo: Optional[str] = None            # Ruta al logo
    
    # === RELACIONES ===
    # Relación uno-a-muchos: Una institución tiene múltiples cursos
    cursos: List["Curso"] = Relationship(back_populates="institucion")
    
    # Relación uno-a-muchos: Una institución tiene múltiples usuarios administradores
    usuarios: List["Usuario"] = Relationship(back_populates="institucion")

# ================================================================================
# MODELO USUARIO - Administradores del sistema
# ================================================================================
class Usuario(SQLModel, table=True):
    """
    Representa un usuario administrador del sistema.
    
    Cada usuario pertenece a una institución específica y puede gestionar
    únicamente los cursos de su institución.
    
    CAMPOS:
    - id: Clave primaria autoincremental
    - correo: Email único del usuario (usado para login)
    - password_hash: Contraseña hasheada con bcrypt
    - institucion_id: Foreign key hacia la institución
    
    RELACIONES:
    - institucion: Institución a la que pertenece el usuario
    
    SEGURIDAD:
    - Las contraseñas se almacenan hasheadas con bcrypt
    - Cada usuario solo puede gestionar cursos de su institución
    - La autenticación se valida en state.py
    
    UTILIZADO EN:
    - pages/login.py: Formulario de autenticación
    - pages/admin.py: Panel de administración por institución
    - state.py: Gestión de sesión y autenticación
    - database.py: Validación de credenciales
    """
    __tablename__ = "usuarios"
    
    # === CAMPOS PRINCIPALES ===
    id: Optional[int] = Field(default=None, primary_key=True)
    correo: str = Field(unique=True, index=True)    # Email único para login
    password_hash: str                              # Contraseña hasheada con bcrypt
    institucion_id: int = Field(foreign_key="instituciones.id")  # FK a institución
    
    # === RELACIONES ===
    # Relación muchos-a-uno: Múltiples usuarios pueden pertenecer a una institución
    institucion: Institucion = Relationship(back_populates="usuarios")

# ================================================================================
# MODELO CURSO - Oferta educativa de cada institución
# ================================================================================
class Curso(SQLModel, table=True):
    """
    Representa un curso ofrecido por una institución educativa.
    
    Los cursos son la información principal que consultan los ciudadanos
    de Salto para conocer la oferta educativa disponible.
    
    CAMPOS:
    - id: Clave primaria autoincremental
    - nombre: Nombre del curso (ej: "Licenciatura en Informática")
    - nivel: Nivel educativo (Bachillerato, Terciario, Universitario, Posgrado)
    - duracion_numero: Duración numérica (1-12)
    - duracion_unidad: Unidad de tiempo (meses, años)
    - requisitos_ingreso: Requisitos previos necesarios
    - informacion: Información adicional, enlaces, descripción detallada
    - institucion_id: Foreign key hacia la institución que lo ofrece
    
    RELACIONES:
    - institucion: Institución que ofrece el curso
    
    VALIDACIONES:
    - Los valores están restringidos por constants.py
    - Se validan en database.py antes de persistir
    
    UTILIZADO EN:
    - pages/cursos.py: Buscador público con filtros
    - pages/admin.py: CRUD de cursos por institución
    - state.py: Filtrado y gestión de datos
    - database.py: Operaciones CRUD con validaciones
    """
    __tablename__ = "cursos"
    
    # === CAMPOS PRINCIPALES ===
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str                                     # Nombre del curso
    nivel: str                                      # Nivel educativo
    duracion_numero: str                            # Duración numérica
    duracion_unidad: str                            # Unidad de tiempo
    requisitos_ingreso: str                         # Requisitos previos
    informacion: Optional[str] = None               # Información adicional
    institucion_id: int = Field(foreign_key="instituciones.id")  # FK a institución
    
    # === RELACIONES ===
    # Relación muchos-a-uno: Múltiples cursos pueden pertenecer a una institución
    institucion: Institucion = Relationship(back_populates="cursos")

# ================================================================================
# NOTAS IMPORTANTES SOBRE SQLMODEL
# ================================================================================
# 
# GESTIÓN AUTOMÁTICA DE REFERENCIAS:
# SQLModel maneja automáticamente las referencias circulares cuando se usan
# strings en los Relationships (ej: "Curso", "Usuario").
# 
# NO ES NECESARIO:
# - Llamar update_forward_refs() manualmente
# - Gestionar referencias circulares
# - Configurar back_populates manualmente si no se requiere navegación bidireccional
#
# MIGRACIONES:
# - Las migraciones se gestionan con Alembic
# - Los cambios en estos modelos requieren: reflex db makemigrations
# - Aplicar cambios con: reflex db migrate
#
# SEED DATA:
# - Los datos iniciales se cargan con seed.py
# - Utiliza estas estructuras para crear instituciones, usuarios y cursos base
