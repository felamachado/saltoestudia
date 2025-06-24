# saltoestudia/database.py

import os
import reflex as rx
from sqlmodel import create_engine, select, Session
from sqlalchemy.orm import selectinload
from typing import List, Optional, Dict, Any
from .models import Institucion, Curso, Usuario
from .constants import ValidationConstants

# --- Creación del Engine de SQLAlchemy ---
# Se usará tanto para el seed como para la app de Reflex
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///reflex.db")
engine = create_engine(DATABASE_URL)

def get_session():
    """Función para obtener una sesión de la base de datos."""
    with Session(engine) as session:
        yield session

def obtener_instituciones() -> List[Dict[str, Any]]:
    """Obtiene todas las instituciones de forma segura, evitando la recursión."""
    try:
        with Session(engine) as session:
            # CORRECCIÓN: Query más simple sin eager loading problemático
            query = select(
                Institucion.id,
                Institucion.nombre,
                Institucion.direccion,
                Institucion.telefono,
                Institucion.email,
                Institucion.web,
                Institucion.logo
            )
            result = session.exec(query).all()
            
            # Construimos manualmente la lista de diccionarios
            instituciones_list = []
            for row in result:
                instituciones_list.append({
                    "id": row[0],
                    "nombre": row[1],
                    "direccion": row[2],
                    "telefono": row[3],
                    "email": row[4],
                    "web": row[5],
                    "logo": row[6] or "/logos/logoutu.png",  # Fallback por defecto
                })
            print("[LOG] Instituciones obtenidas de la BBDD:", instituciones_list)
            return instituciones_list
    except Exception as e:
        print(f"Error al obtener instituciones: {e}")
        # Retornamos lista vacía en caso de error
        return []

def obtener_instituciones_nombres() -> List[str]:
    """Obtiene solo los nombres de las instituciones."""
    try:
        with Session(engine) as session:
            query = select(Institucion.nombre).distinct()
            results = session.exec(query).all()
            return [r for r in results]
    except Exception as e:
        print(f"Error al obtener nombres de instituciones: {e}")
        return []

def obtener_cursos() -> List[Dict[str, Any]]:
    """Obtiene todos los cursos con sus datos relacionados de forma segura."""
    try:
        with Session(engine) as session:
            cursos_db = session.exec(select(Curso)).all()
            cursos_list = []
            for curso in cursos_db:
                institucion = session.get(Institucion, curso.institucion_id) if curso.institucion_id else None
                
                cursos_list.append({
                    "id": curso.id,
                    "nombre": curso.nombre,
                    "nivel": curso.nivel or "N/A",
                    "requisitos_ingreso": curso.requisitos_ingreso or "N/A",
                    "duracion_numero": curso.duracion_numero,
                    "duracion_unidad": curso.duracion_unidad,
                    "informacion": curso.informacion,
                    "institucion": institucion.nombre if institucion else "N/A",
                })
            print(f"[LOG] Cursos obtenidos: {len(cursos_list)}")
            return cursos_list
    except Exception as e:
        print(f"Error al obtener cursos: {e}")
        return []

def obtener_niveles() -> List[str]:
    """Obtiene la lista de niveles educativos únicos desde las constantes."""
    try:
        from .constants import CursosConstants
        return CursosConstants.NIVELES
    except Exception as e:
        print(f"Error al obtener niveles: {e}")
        return ["Bachillerato", "Terciario", "Universitario"]

def obtener_requisitos() -> List[str]:
    """Obtiene la lista de requisitos de ingreso únicos desde las constantes."""
    try:
        from .constants import CursosConstants
        return CursosConstants.REQUISITOS_INGRESO
    except Exception as e:
        print(f"Error al obtener requisitos: {e}")
        return ["Ciclo básico", "Bachillerato", "Terciario"]

def obtener_nombre_institucion_por_id(institucion_id: int) -> str:
    """Obtiene el nombre de una institución por su ID."""
    try:
        with Session(engine) as session:
            institucion = session.get(Institucion, institucion_id)
            return institucion.nombre if institucion else "Institución no encontrada"
    except Exception as e:
        print(f"Error al obtener nombre de institución: {e}")
        return "Error al obtener institución"

def obtener_usuario_por_correo(correo: str) -> Optional[Usuario]:
    """Obtiene un usuario por su correo, cargando su institución de forma eagerly."""
    try:
        with Session(engine) as session:
            # Usar selectinload para cargar la relación 'institucion' en la misma consulta
            # y evitar errores de 'DetachedInstanceError'
            statement = select(Usuario).options(selectinload(Usuario.institucion)).where(Usuario.correo == correo)
            usuario = session.exec(statement).one_or_none()
            return usuario
    except Exception as e:
        print(f"Error al obtener usuario por correo: {e}")
        return None

def obtener_cursos_por_institucion(institucion_id: int) -> List[Dict[str, Any]]:
    """Obtiene todos los cursos de una institución específica por su ID."""
    try:
        with Session(engine) as session:
            # Obtener institución por ID
            institucion = session.get(Institucion, institucion_id)
            
            if not institucion:
                print(f"[LOG] Institución no encontrada con ID: {institucion_id}")
                return []

            cursos_db = session.exec(
                select(Curso).where(Curso.institucion_id == institucion_id)
            ).all()
            
            cursos_list = []
            for curso in cursos_db:
                cursos_list.append({
                    "id": curso.id,
                    "nombre": curso.nombre,
                    "nivel": curso.nivel or "N/A",
                    "requisitos_ingreso": curso.requisitos_ingreso or "N/A",
                    "duracion_numero": curso.duracion_numero,
                    "duracion_unidad": curso.duracion_unidad,
                    "informacion": curso.informacion,
                    "institucion": institucion.nombre,
                })
            print(f"[LOG] Cursos obtenidos para institución {institucion.nombre} (ID: {institucion_id}): {len(cursos_list)}")
            return cursos_list
    except Exception as e:
        print(f"Error al obtener cursos por institucion: {e}")
        return []

def agregar_curso(datos_curso: dict):
    """Agrega un nuevo curso a la base de datos."""
    try:
        # Validar datos usando las constantes
        if not ValidationConstants.validate_nivel(datos_curso.get("nivel", "")):
            raise ValueError(f"Nivel inválido: {datos_curso.get('nivel')}")
        
        if not ValidationConstants.validate_duracion_numero(datos_curso.get("duracion_numero", "")):
            raise ValueError(f"Duración número inválido: {datos_curso.get('duracion_numero')}")
        
        if not ValidationConstants.validate_duracion_unidad(datos_curso.get("duracion_unidad", "")):
            raise ValueError(f"Duración unidad inválida: {datos_curso.get('duracion_unidad')}")
        
        if not ValidationConstants.validate_requisitos(datos_curso.get("requisitos_ingreso", "")):
            raise ValueError(f"Requisito inválido: {datos_curso.get('requisitos_ingreso')}")

        with Session(engine) as session:
            # Crear nuevo curso usando institucion_id directamente
            nuevo_curso = Curso(
                nombre=datos_curso.get("nombre"),
                nivel=datos_curso.get("nivel"),
                duracion_numero=datos_curso.get("duracion_numero"),
                duracion_unidad=datos_curso.get("duracion_unidad"),
                requisitos_ingreso=datos_curso.get("requisitos_ingreso"),
                informacion=datos_curso.get("informacion"),
                institucion_id=datos_curso.get("institucion_id")
            )
            
            session.add(nuevo_curso)
            session.commit()
            print(f"Curso agregado exitosamente: {datos_curso}")
            
    except Exception as e:
        print(f"Error al agregar curso: {e}")
        raise e

def modificar_curso(curso_id: int, datos_curso: dict):
    """Modifica un curso existente en la base de datos."""
    try:
        # Validar datos usando las constantes
        if datos_curso.get("nivel") and not ValidationConstants.validate_nivel(datos_curso.get("nivel")):
            raise ValueError(f"Nivel inválido: {datos_curso.get('nivel')}")
        
        if datos_curso.get("duracion_numero") and not ValidationConstants.validate_duracion_numero(datos_curso.get("duracion_numero")):
            raise ValueError(f"Duración número inválido: {datos_curso.get('duracion_numero')}")
        
        if datos_curso.get("duracion_unidad") and not ValidationConstants.validate_duracion_unidad(datos_curso.get("duracion_unidad")):
            raise ValueError(f"Duración unidad inválida: {datos_curso.get('duracion_unidad')}")
        
        if datos_curso.get("requisitos_ingreso") and not ValidationConstants.validate_requisitos(datos_curso.get("requisitos_ingreso")):
            raise ValueError(f"Requisito inválido: {datos_curso.get('requisitos_ingreso')}")

        with Session(engine) as session:
            curso = session.get(Curso, curso_id)
            if not curso:
                raise ValueError(f"Curso no encontrado con ID: {curso_id}")
            
            # Actualizar campos
            if "nombre" in datos_curso:
                curso.nombre = datos_curso["nombre"]
            if "nivel" in datos_curso:
                curso.nivel = datos_curso["nivel"]
            if "duracion_numero" in datos_curso:
                curso.duracion_numero = datos_curso["duracion_numero"]
            if "duracion_unidad" in datos_curso:
                curso.duracion_unidad = datos_curso["duracion_unidad"]
            if "requisitos_ingreso" in datos_curso:
                curso.requisitos_ingreso = datos_curso["requisitos_ingreso"]
            if "informacion" in datos_curso:
                curso.informacion = datos_curso["informacion"]
            
            session.add(curso)
            session.commit()
            print(f"Curso {curso_id} modificado exitosamente: {datos_curso}")
            
    except Exception as e:
        print(f"Error al modificar curso: {e}")
        raise e

def eliminar_curso(curso_id: int):
    """Elimina un curso de la base de datos por su ID."""
    try:
        with Session(engine) as session:
            curso = session.get(Curso, curso_id)
            if not curso:
                raise ValueError(f"Curso no encontrado con ID: {curso_id}")
            
            session.delete(curso)
            session.commit()
            print(f"Curso {curso_id} eliminado exitosamente")
            
    except Exception as e:
        print(f"Error al eliminar curso: {e}")
        raise e
