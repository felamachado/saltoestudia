# saltoestudia/models.py

from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship

# --- Modelo Institucion ---
class Institucion(SQLModel, table=True):
    __tablename__ = "instituciones"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[str] = None
    web: Optional[str] = None
    logo: Optional[str] = None
    
    # Relación uno-a-muchos con Curso
    cursos: List["Curso"] = Relationship(back_populates="institucion")
    
    # Relación uno-a-muchos con Usuario
    usuarios: List["Usuario"] = Relationship(back_populates="institucion")

# --- Modelo Usuario ---
class Usuario(SQLModel, table=True):
    __tablename__ = "usuarios"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    correo: str = Field(unique=True, index=True)
    password_hash: str
    institucion_id: int = Field(foreign_key="instituciones.id")
    
    # Relación muchos-a-uno con Institucion
    institucion: Institucion = Relationship(back_populates="usuarios")

# --- Modelo Curso ---
class Curso(SQLModel, table=True):
    __tablename__ = "cursos"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    nivel: str
    duracion_numero: str
    duracion_unidad: str
    requisitos_ingreso: str
    informacion: Optional[str] = None
    institucion_id: int = Field(foreign_key="instituciones.id")
    
    # Relación muchos-a-uno con Institucion
    institucion: Institucion = Relationship(back_populates="cursos")

# --- Actualizar referencias ---
# Esto es crucial para resolver las referencias circulares ("Curso", "Usuario", "Institucion")
Institucion.update_forward_refs(Curso=Curso, Usuario=Usuario)
Usuario.update_forward_refs(Institucion=Institucion)
Curso.update_forward_refs(Institucion=Institucion)

# NOTA: Eliminamos las tablas Nivel y RequisitoIngreso ya que ahora usamos constantes hardcodeadas
