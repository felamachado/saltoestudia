# saltoestudia/database.py

# ================================================================================
# OPERACIONES DE BASE DE DATOS - SALTO ESTUDIA
# ================================================================================
#
# Este archivo centraliza todas las operaciones de base de datos del sistema,
# proporcionando una capa de abstracción entre los modelos SQLModel y la UI.
#
# ARQUITECTURA:
# - Engine único compartido entre seed.py y la aplicación Reflex
# - Sesiones de corta duración con patrón context manager
# - Validaciones usando constants.py antes de persistir
# - Manejo de errores robusto con logging
#
# OPERACIONES PRINCIPALES:
# 1. LECTURA: obtener_instituciones, obtener_cursos, obtener_usuarios
# 2. ESCRITURA: agregar_curso, modificar_curso, eliminar_curso  
# 3. VALIDACIÓN: Usando ValidationConstants para integridad de datos
# 4. AUTENTICACIÓN: obtener_usuario_por_correo con eager loading
#
# UTILIZADO POR:
# - state.py: Para todas las operaciones de datos desde la UI
# - pages/admin.py: CRUD de cursos por institución
# - pages/cursos.py: Consultas públicas con filtros
# - seed.py: Poblado inicial de datos
# ================================================================================

import os
import reflex as rx
from sqlmodel import create_engine, select, Session
from sqlalchemy.orm import selectinload
from typing import List, Optional, Dict, Any
from .models import Institucion, Curso, Usuario
from .constants import ValidationConstants

# ================================================================================
# CONFIGURACIÓN DEL ENGINE DE BASE DE DATOS
# ================================================================================

# === ENGINE GLOBAL ===
# Engine único compartido entre la aplicación y los scripts de seed
# Usa la variable de entorno DATABASE_URL o fallback a SQLite por defecto
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///reflex.db")
engine = create_engine(DATABASE_URL)

def get_session():
    """
    Generador de sesiones de base de datos.
    
    Proporciona una sesión SQLAlchemy con manejo automático del ciclo de vida.
    Utiliza el patrón context manager para asegurar que las sesiones se cierren
    correctamente incluso si ocurren errores.
    
    Yields:
        Session: Sesión de SQLAlchemy lista para usar
        
    Uso:
        with get_session() as session:
            # Operaciones de base de datos
            pass
    
    NOTA: Actualmente no se usa en el código, pero está disponible para
    operaciones más complejas que requieran manejo manual de sesiones.
    """
    with Session(engine) as session:
        yield session

# ================================================================================
# OPERACIONES DE LECTURA - INSTITUCIONES
# ================================================================================

def obtener_instituciones() -> List[Dict[str, Any]]:
    """
    Obtiene todas las instituciones educativas del sistema.
    
    Esta función es crítica para la página de instituciones y los filtros
    de cursos. Utiliza una query optimizada sin eager loading para evitar
    problemas de recursión con las relaciones.
    
    Returns:
        List[Dict]: Lista de diccionarios con datos de instituciones
                   Incluye fallback para logos faltantes
    
    Estructura de retorno:
        [
            {
                "id": 1,
                "nombre": "UDELAR – CENUR LN",
                "direccion": "Rivera 1350",
                "telefono": "47334816",
                "email": "comunicacion@unorte.edu.uy",
                "web": "https://www.litoralnorte.udelar.edu.uy/",
                "logo": "/logos/logo-cenur.png"
            },
            ...
        ]
    
    Utilizado en:
        - state.py: cargar_instituciones() para la galería
        - pages/instituciones.py: Mostrar tarjetas de instituciones
        - Inicialización de datos para filtros
    
    Optimizaciones:
        - Query directa sin joins innecesarios
        - Construcción manual de diccionarios para control total
        - Fallback automático para logos faltantes
    """
    try:
        with Session(engine) as session:
            # === QUERY OPTIMIZADA ===
            # Selección directa de campos sin eager loading problemático
            # Evita cargar relaciones innecesarias que pueden causar recursión
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
            
            # === CONSTRUCCIÓN DE RESPUESTA ===
            # Construcción manual para control total sobre el formato
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
            print(f"[LOG] Instituciones obtenidas de la BBDD: {len(instituciones_list)}")
            return instituciones_list
    except Exception as e:
        print(f"[ERROR] Error al obtener instituciones: {e}")
        # Retorno seguro en caso de error - evita crashes de la UI
        return []

def obtener_instituciones_nombres() -> List[str]:
    """
    Obtiene solo los nombres de las instituciones para filtros y dropdowns.
    
    Función optimizada para poblar selectores en la UI sin cargar datos
    innecesarios. Especialmente útil para filtros donde solo se necesita
    el nombre para la comparación.
    
    Returns:
        List[str]: Lista de nombres de instituciones
                  Ejemplo: ["UDELAR – CENUR LN", "IAE Salto", ...]
    
    Utilizado en:
        - state.py: cargar_instituciones_nombres() para filtros
        - pages/cursos.py: Dropdown de filtro por institución
        - Formularios que requieren selección de institución
    
    Optimización:
        - Solo carga el campo 'nombre', no toda la entidad
        - Usa DISTINCT para evitar duplicados (aunque no debería haberlos)
    """
    try:
        with Session(engine) as session:
            # Query minimalista - solo nombres únicos
            query = select(Institucion.nombre).distinct()
            results = session.exec(query).all()
            return [r for r in results]  # Conversión a lista simple
    except Exception as e:
        print(f"[ERROR] Error al obtener nombres de instituciones: {e}")
        return []  # Retorno seguro

# ================================================================================
# OPERACIONES DE LECTURA - CURSOS
# ================================================================================

def obtener_cursos() -> List[Dict[str, Any]]:
    """
    Obtiene todos los cursos del sistema con información de la institución.
    
    Esta es la función principal para la página pública de cursos. Carga todos
    los cursos disponibles y los enriquece con el nombre de la institución
    para mostrar información completa al usuario.
    
    Returns:
        List[Dict]: Lista de cursos con datos relacionados
    
    Estructura de retorno:
        [
            {
                "id": 1,
                "nombre": "Licenciatura en Informática",
                "nivel": "Universitario",
                "requisitos_ingreso": "Bachillerato",
                "duracion_numero": "4",
                "duracion_unidad": "años",
                "informacion": "Programa con fuerte énfasis...",
                "institucion": "UDELAR – CENUR LN"
            },
            ...
        ]
    
    Utilizado en:
        - state.py: cargar_cursos() para el buscador público
        - pages/cursos.py: Datos para AG Grid y tabla
        - Filtros y búsquedas en tiempo real
    
    Patrón de carga:
        - Carga todos los cursos primero
        - Hace queries individuales para instituciones (N+1 controlado)
        - Fallback seguro para datos faltantes
    """
    try:
        with Session(engine) as session:
            # === CARGA INICIAL ===
            # Obtener todos los cursos de la base de datos
            cursos_db = session.exec(select(Curso)).all()
            cursos_list = []
            
            # === ENRIQUECIMIENTO DE DATOS ===
            # Para cada curso, obtener el nombre de su institución
            for curso in cursos_db:
                # Query individual para institución (patrón N+1 controlado)
                institucion = session.get(Institucion, curso.institucion_id) if curso.institucion_id else None
                
                # Construcción del diccionario de respuesta
                cursos_list.append({
                    "id": curso.id,
                    "nombre": curso.nombre,
                    "nivel": curso.nivel or "N/A",                    # Fallback para datos faltantes
                    "requisitos_ingreso": curso.requisitos_ingreso or "N/A",
                    "duracion_numero": curso.duracion_numero,
                    "duracion_unidad": curso.duracion_unidad,
                    "informacion": curso.informacion,
                    "institucion": institucion.nombre if institucion else "N/A",  # Fallback seguro
                })
            
            print(f"[LOG] Cursos obtenidos: {len(cursos_list)}")
            return cursos_list
    except Exception as e:
        print(f"[ERROR] Error al obtener cursos: {e}")
        return []  # Retorno seguro

def obtener_cursos_por_institucion(institucion_id: int) -> List[Dict[str, Any]]:
    """
    Obtiene todos los cursos de una institución específica.
    
    Función crítica para el panel de administración. Permite a cada usuario
    administrador ver y gestionar únicamente los cursos de su institución,
    implementando así el aislamiento de datos por institución.
    
    Args:
        institucion_id: ID de la institución cuyos cursos se quieren obtener
    
    Returns:
        List[Dict]: Lista de cursos de la institución especificada
                   Retorna lista vacía si la institución no existe
    
    Utilizado en:
        - state.py: cargar_cursos_admin() para el panel administrativo
        - pages/admin.py: Tabla de cursos del administrador logueado
        - Operaciones CRUD que requieren verificar pertenencia
    
    Seguridad:
        - Verifica que la institución exista antes de proceder
        - Solo retorna cursos de la institución específica
        - Logging detallado para auditoría
    """
    try:
        with Session(engine) as session:
            # === VERIFICACIÓN DE INSTITUCIÓN ===
            # Verificar que la institución existe antes de buscar cursos
            institucion = session.get(Institucion, institucion_id)
            
            if not institucion:
                print(f"[LOG] Institución no encontrada con ID: {institucion_id}")
                return []

            # === QUERY FILTRADA ===
            # Obtener solo cursos de la institución específica
            cursos_db = session.exec(
                select(Curso).where(Curso.institucion_id == institucion_id)
            ).all()
            
            # === CONSTRUCCIÓN DE RESPUESTA ===
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
                    "institucion": institucion.nombre,  # Ya verificamos que existe
                })
            
            print(f"[LOG] Cursos obtenidos para institución {institucion.nombre} (ID: {institucion_id}): {len(cursos_list)}")
            return cursos_list
    except Exception as e:
        print(f"[ERROR] Error al obtener cursos por institución: {e}")
        return []

# ================================================================================
# FUNCIONES DE COMPATIBILIDAD - CONSTANTES DINÁMICAS
# ================================================================================

def obtener_niveles() -> List[str]:
    """
    Obtiene la lista de niveles educativos desde las constantes.
    
    NOTA: Esta función está marcada para refactoring. Actualmente devuelve
    los valores de CursosConstants.NIVELES, pero existe para mantener
    compatibilidad con código legacy que esperaba obtener estos valores
    dinámicamente desde la base de datos.
    
    Returns:
        List[str]: Lista de niveles educativos disponibles
    
    TODO: Eliminar esta función y usar directamente CursosConstants.NIVELES
    en el código que la consume.
    """
    try:
        from .constants import CursosConstants
        return CursosConstants.NIVELES
    except Exception as e:
        print(f"[ERROR] Error al obtener niveles: {e}")
        # Fallback hardcodeado para casos de emergencia
        return ["Bachillerato", "Terciario", "Universitario"]

def obtener_requisitos() -> List[str]:
    """
    Obtiene la lista de requisitos de ingreso desde las constantes.
    
    NOTA: Similar a obtener_niveles(), existe para compatibilidad.
    El patrón recomendado es usar directamente CursosConstants.REQUISITOS_INGRESO.
    
    Returns:
        List[str]: Lista de requisitos de ingreso disponibles
    
    TODO: Eliminar y usar constantes directamente.
    """
    try:
        from .constants import CursosConstants
        return CursosConstants.REQUISITOS_INGRESO
    except Exception as e:
        print(f"[ERROR] Error al obtener requisitos: {e}")
        # Fallback hardcodeado
        return ["Ciclo básico", "Bachillerato", "Terciario"]

# ================================================================================
# OPERACIONES DE LECTURA - USUARIOS Y AUTENTICACIÓN
# ================================================================================

def obtener_nombre_institucion_por_id(institucion_id: int) -> str:
    """
    Obtiene el nombre de una institución por su ID.
    
    Función utilitaria para resolver nombres de instituciones en contextos
    donde solo se tiene el ID disponible.
    
    Args:
        institucion_id: ID de la institución
    
    Returns:
        str: Nombre de la institución o mensaje de error
    
    Utilizado en:
        - Logs y debugging
        - Resolución de nombres en contextos administrativos
        - Validaciones que requieren mostrar nombres legibles
    """
    try:
        with Session(engine) as session:
            institucion = session.get(Institucion, institucion_id)
            return institucion.nombre if institucion else "Institución no encontrada"
    except Exception as e:
        print(f"[ERROR] Error al obtener nombre de institución: {e}")
        return "Error al obtener institución"

def obtener_usuario_por_correo(correo: str) -> Optional[Usuario]:
    """
    Obtiene un usuario por su correo electrónico con carga eager de institución.
    
    Esta función es CRÍTICA para el sistema de autenticación. Utiliza
    selectinload para cargar la institución del usuario en la misma query,
    evitando el error DetachedInstanceError que ocurre cuando se accede
    a relaciones después de cerrar la sesión.
    
    Args:
        correo: Email del usuario a buscar
    
    Returns:
        Optional[Usuario]: Usuario con institución cargada o None si no existe
    
    Utilizado en:
        - state.py: handle_login() y handle_login_redirect()
        - Validación de credenciales en el proceso de autenticación
        - Verificación de existencia de usuarios
    
    Patrón crítico:
        - selectinload(Usuario.institucion) carga la relación en la misma query
        - Evita lazy loading que fallaría después del cierre de sesión
        - Permite acceso a usuario.institucion.nombre fuera de la sesión
    
    Seguridad:
        - Solo busca por correo, no valida contraseña (eso se hace en state.py)
        - Retorna None si no encuentra usuario (no revela información)
    """
    try:
        with Session(engine) as session:
            # === QUERY CON EAGER LOADING ===
            # selectinload es CRÍTICO para cargar la relación institución
            # en la misma query y evitar DetachedInstanceError
            statement = select(Usuario).options(selectinload(Usuario.institucion)).where(Usuario.correo == correo)
            usuario = session.exec(statement).one_or_none()
            return usuario
    except Exception as e:
        print(f"[ERROR] Error al obtener usuario por correo: {e}")
        return None

# ================================================================================
# OPERACIONES DE ESCRITURA - CRUD DE CURSOS
# ================================================================================

def agregar_curso(datos_curso: dict):
    """
    Agrega un nuevo curso a la base de datos con validaciones completas.
    
    Esta función implementa el CREATE del CRUD para cursos. Incluye validaciones
    estrictas usando ValidationConstants para asegurar la integridad de datos
    antes de la persistencia.
    
    Args:
        datos_curso: Diccionario con los datos del curso a crear
                    Ejemplo: {
                        "nombre": "Licenciatura en Informática",
                        "nivel": "Universitario",
                        "duracion_numero": "4",
                        "duracion_unidad": "años",
                        "requisitos_ingreso": "Bachillerato",
                        "informacion": "Programa con fuerte énfasis...",
                        "institucion_id": 1
                    }
    
    Raises:
        ValueError: Si algún campo no cumple las validaciones
        Exception: Para otros errores de base de datos
    
    Utilizado en:
        - state.py: guardar_curso() cuando is_editing=False
        - pages/admin.py: Formulario de agregar nuevo curso
        - Operaciones de importación masiva de datos
    
    Validaciones aplicadas:
        - nivel debe estar en CursosConstants.NIVELES
        - duracion_numero debe estar en rango 1-12
        - duracion_unidad debe ser "meses" o "años"
        - requisitos_ingreso debe estar en CursosConstants.REQUISITOS_INGRESO
    
    Patrón de seguridad:
        - Validación ANTES de crear la entidad
        - Transacción implícita con commit al final
        - Logging detallado para auditoría
        - Re-raise de excepciones para manejo en UI
    """
    try:
        # === VALIDACIONES PRE-PERSISTENCIA ===
        # Validar todos los campos críticos antes de crear el objeto
        if not ValidationConstants.validate_nivel(datos_curso.get("nivel", "")):
            raise ValueError(f"Nivel inválido: {datos_curso.get('nivel')}")
        
        if not ValidationConstants.validate_duracion_numero(datos_curso.get("duracion_numero", "")):
            raise ValueError(f"Duración número inválido: {datos_curso.get('duracion_numero')}")
        
        if not ValidationConstants.validate_duracion_unidad(datos_curso.get("duracion_unidad", "")):
            raise ValueError(f"Duración unidad inválida: {datos_curso.get('duracion_unidad')}")
        
        if not ValidationConstants.validate_requisitos(datos_curso.get("requisitos_ingreso", "")):
            raise ValueError(f"Requisito inválido: {datos_curso.get('requisitos_ingreso')}")

        with Session(engine) as session:
            # === CREACIÓN DE ENTIDAD ===
            # Crear nueva instancia del modelo con datos validados
            nuevo_curso = Curso(
                nombre=datos_curso.get("nombre"),
                nivel=datos_curso.get("nivel"),
                duracion_numero=datos_curso.get("duracion_numero"),
                duracion_unidad=datos_curso.get("duracion_unidad"),
                requisitos_ingreso=datos_curso.get("requisitos_ingreso"),
                informacion=datos_curso.get("informacion"),
                institucion_id=datos_curso.get("institucion_id")  # FK ya validada por constraints
            )
            
            # === PERSISTENCIA ===
            session.add(nuevo_curso)
            session.commit()  # Persistir en base de datos
            print(f"[LOG] Curso agregado exitosamente: {datos_curso.get('nombre')}")
            
    except Exception as e:
        print(f"[ERROR] Error al agregar curso: {e}")
        raise e  # Re-raise para manejo en state.py

def modificar_curso(curso_id: int, datos_curso: dict):
    """
    Modifica un curso existente en la base de datos.
    
    Esta función implementa el UPDATE del CRUD para cursos. Permite actualización
    parcial de campos (solo los campos presentes en datos_curso se modifican).
    Incluye las mismas validaciones que agregar_curso.
    
    Args:
        curso_id: ID del curso a modificar
        datos_curso: Diccionario con los campos a actualizar
                    Solo los campos presentes se modificarán
    
    Raises:
        ValueError: Si el curso no existe o si algún campo no es válido
        Exception: Para otros errores de base de datos
    
    Utilizado en:
        - state.py: guardar_curso() cuando is_editing=True
        - pages/admin.py: Formulario de edición de curso existente
        - Operaciones de actualización masiva
    
    Patrón de actualización:
        - Verificación de existencia del curso
        - Validación solo de campos presentes
        - Actualización campo por campo con condicionales
        - Commit solo si todo es exitoso
    
    Seguridad:
        - No permite cambiar institucion_id (protege aislamiento de datos)
        - Validación igual que en creación
        - Logging detallado con ID del curso modificado
    """
    try:
        # === VALIDACIONES CONDICIONALES ===
        # Solo validar campos que están presentes en la actualización
        if datos_curso.get("nivel") and not ValidationConstants.validate_nivel(datos_curso.get("nivel")):
            raise ValueError(f"Nivel inválido: {datos_curso.get('nivel')}")
        
        if datos_curso.get("duracion_numero") and not ValidationConstants.validate_duracion_numero(datos_curso.get("duracion_numero")):
            raise ValueError(f"Duración número inválido: {datos_curso.get('duracion_numero')}")
        
        if datos_curso.get("duracion_unidad") and not ValidationConstants.validate_duracion_unidad(datos_curso.get("duracion_unidad")):
            raise ValueError(f"Duración unidad inválida: {datos_curso.get('duracion_unidad')}")
        
        if datos_curso.get("requisitos_ingreso") and not ValidationConstants.validate_requisitos(datos_curso.get("requisitos_ingreso")):
            raise ValueError(f"Requisito inválido: {datos_curso.get('requisitos_ingreso')}")

        with Session(engine) as session:
            # === VERIFICACIÓN DE EXISTENCIA ===
            curso = session.get(Curso, curso_id)
            if not curso:
                raise ValueError(f"Curso no encontrado con ID: {curso_id}")
            
            # === ACTUALIZACIÓN CONDICIONAL ===
            # Solo actualizar campos que están presentes en datos_curso
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
            # NOTA: No permitimos cambiar institucion_id por seguridad
            
            # === PERSISTENCIA ===
            session.add(curso)  # Marca el objeto como modificado
            session.commit()
            print(f"[LOG] Curso {curso_id} modificado exitosamente: {curso.nombre}")
            
    except Exception as e:
        print(f"[ERROR] Error al modificar curso: {e}")
        raise e  # Re-raise para manejo en state.py

def eliminar_curso(curso_id: int):
    """
    Elimina un curso de la base de datos por su ID.
    
    Esta función implementa el DELETE del CRUD para cursos. Es una operación
    crítica que requiere confirmación del usuario en la UI.
    
    Args:
        curso_id: ID del curso a eliminar
    
    Raises:
        ValueError: Si el curso no existe
        Exception: Para otros errores de base de datos
    
    Utilizado en:
        - state.py: confirmar_eliminacion() después de confirmación del usuario
        - pages/admin.py: Botón de eliminar con diálogo de confirmación
        - Operaciones de limpieza de datos
    
    Seguridad:
        - Verificación de existencia antes de eliminar
        - Eliminación física (no soft delete)
        - Logging detallado para auditoría
        - No permite deshacer la operación
    
    IMPORTANTE:
        Esta operación es irreversible. La UI debe implementar
        confirmaciones apropiadas antes de llamar esta función.
    """
    try:
        with Session(engine) as session:
            # === VERIFICACIÓN DE EXISTENCIA ===
            curso = session.get(Curso, curso_id)
            if not curso:
                raise ValueError(f"Curso no encontrado con ID: {curso_id}")
            
            # === ELIMINACIÓN FÍSICA ===
            # Eliminar permanentemente de la base de datos
            nombre_curso = curso.nombre  # Guardar para logging
            session.delete(curso)
            session.commit()
            print(f"[LOG] Curso {curso_id} ({nombre_curso}) eliminado exitosamente")
            
    except Exception as e:
        print(f"[ERROR] Error al eliminar curso: {e}")
        raise e  # Re-raise para manejo en state.py

# ================================================================================
# NOTAS IMPORTANTES SOBRE OPERACIONES CRUD
# ================================================================================
#
# TRANSACCIONES:
# - Cada operación usa su propia sesión y transacción
# - Commit automático al final de operaciones exitosas
# - Rollback automático en caso de excepción
#
# VALIDACIONES:
# - Todas las validaciones se centralizan en ValidationConstants
# - Se valida ANTES de crear/modificar objetos
# - Errores de validación se propagan como ValueError
#
# LOGGING:
# - Todas las operaciones incluyen logging detallado
# - Formato: [LOG] para éxito, [ERROR] para fallos
# - Incluye información contextual (ID, nombre, etc.)
#
# MANEJO DE ERRORES:
# - Re-raise de excepciones para manejo en state.py
# - state.py puede mostrar errores amigables al usuario
# - No se capturan excepciones internamente para debugging
#
# SEGURIDAD:
# - No se permite cambiar institucion_id en modificaciones
# - Verificación de existencia antes de operaciones
# - No se revelan detalles internos en mensajes de error públicos
