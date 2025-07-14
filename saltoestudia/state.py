# ================================================================================
# GESTIÓN DE ESTADO GLOBAL - SALTO ESTUDIA
# ================================================================================
#
# Este archivo es el NÚCLEO del sistema de gestión de estado reactivo.
# Implementa el patrón State Management de Reflex para manejar toda la lógica
# de negocio, autenticación, filtros y operaciones CRUD.
#
# ARQUITECTURA DE ESTADO:
# - State: Clase principal que hereda de rx.State (singleton global)
# - User: Modelo seguro para usuarios autenticados (sin contraseñas)
# - Estados por funcionalidad: cursos, instituciones, admin, auth
#
# RESPONSABILIDADES PRINCIPALES:
# 1. AUTENTICACIÓN: Login/logout con validación de credenciales
# 2. FILTROS PÚBLICOS: Búsqueda de cursos con múltiples criterios
# 3. ADMIN CRUD: Gestión de cursos por institución (usuarios autenticados)
# 4. NAVEGACIÓN: Control de flujos y redirecciones
# 5. UI STATE: Estados de modales, diálogos y componentes interactivos
#
# PATRONES IMPLEMENTADOS:
# - Reactive State: Cambios automáticos en UI cuando cambia el estado
# - Session Management: Gestión de sesión de usuario sin cookies
# - Data Loading: Carga lazy y eager según necesidades
# - Error Handling: Manejo robusto de errores con fallbacks
# - Security: Aislamiento de datos por institución
#
# CONEXIÓN CON OTROS ARCHIVOS:
# - database.py: Para todas las operaciones de persistencia
# - constants.py: Para validaciones y opciones de formularios
# - pages/*.py: Las páginas consumen y modifican este estado
# ================================================================================

import reflex as rx
import bcrypt
from typing import List, Dict, Any, Optional
from .database import (
    obtener_instituciones,
    obtener_instituciones_nombres,
    obtener_cursos,
    obtener_usuario_por_correo,
    obtener_cursos_por_institucion,
    agregar_curso,
    modificar_curso,
    eliminar_curso,
    obtener_nombre_institucion_por_id,
    obtener_ciudades_nombres,
)
from .models import Usuario
from .constants import CursosConstants

# ================================================================================
# MODELO DE USUARIO SEGURO PARA ESTADO
# ================================================================================

class User(rx.Base):
    """
    Modelo de usuario seguro para el estado de Reflex.
    
    Esta clase define la estructura de datos del usuario autenticado
    que se almacena en el estado global. Excluye información sensible
    como contraseñas y solo mantiene datos necesarios para la UI.
    
    CAMPOS:
    - id: ID único del usuario en la base de datos
    - correo: Email del usuario (usado para mostrar en UI)
    - institucion_id: ID de la institución a la que pertenece
    - institucion_nombre: Nombre de la institución (para mostrar en UI)
    
    SEGURIDAD:
    - NO incluye password_hash ni información sensible
    - Solo datos necesarios para autorización y UI
    - Se reconstruye en cada login desde database.py
    
    UTILIZADO EN:
    - State.logged_in_user: Usuario actualmente autenticado
    - Verificaciones de permisos en páginas protegidas
    - Mostrar información contextual en UI admin
    """
    id: int                      # ID único del usuario
    correo: str                  # Email para mostrar en UI
    institucion_id: int          # ID de institución para filtros CRUD
    institucion_nombre: str      # Nombre para mostrar en header admin

# ================================================================================
# CLASE PRINCIPAL DE ESTADO GLOBAL
# ================================================================================

class State(rx.State):
    """
    Clase principal de gestión de estado global del sistema Salto Estudia.
    
    Esta clase centraliza TODA la lógica de negocio del sistema y define
    los datos reactivos que automáticamente actualizan la UI cuando cambian.
    
    ORGANIZACIÓN POR FUNCIONALIDADES:
    1. CURSOS PÚBLICOS: Búsqueda y filtrado para usuarios no autenticados
    2. INSTITUCIONES: Galería y información de instituciones educativas  
    3. AUTENTICACIÓN: Login, logout y gestión de sesión
    4. ADMIN CRUD: Operaciones de cursos para usuarios autenticados
    5. UI CONTROL: Estados de modales, diálogos y componentes
    
    PATRÓN REACTIVO:
    - Cualquier cambio en estas variables automáticamente actualiza la UI
    - No se requiere refrescar la página manualmente
    - Los componentes se suscriben automáticamente a los cambios
    
    THREAD SAFETY:
    - Reflex garantiza thread safety para todas las operaciones de estado
    - Cada usuario tiene su propia instancia de estado
    - No hay conflictos entre sesiones de usuarios diferentes
    """
    # ================================================================================
    # VARIABLES DE ESTADO - FUNCIONALIDAD CURSOS PÚBLICOS
    # ================================================================================
    
    # === DATOS DE CURSOS ===
    cursos: List[Dict[str, Any]] = []                    # Cursos filtrados mostrados en UI
    cursos_originales: List[Dict[str, Any]] = []         # Todos los cursos sin filtrar (cache)
    tabla_cursos_data: List[List[Any]] = []              # Formato tabla para compatibilidad legacy
    
    # === CACHE Y PERFORMANCE ===
    cursos_cache_loaded: bool = False                    # Flag de cache de cursos cargado
    instituciones_cache_loaded: bool = False             # Flag de cache de instituciones cargado
    ciudades_cache_loaded: bool = False                  # Flag de cache de ciudades cargado
    
    # === FILTROS DE BÚSQUEDA ===
    # Estos filtros se aplican en tiempo real en la página /cursos
    nivel_seleccionado: str = ""                         # Filtro por nivel educativo
    duracion_seleccionada: str = ""                      # Filtro por duración (no implementado completamente)
    requisito_seleccionado: str = ""                     # Filtro por requisitos de ingreso
    institucion_seleccionada: str = ""                   # Filtro por institución
    lugar_seleccionado: str = ""                         # Filtro por lugar
    busqueda_texto: str = ""  # Filtro de búsqueda manual
    
    # === DATOS DE INSTITUCIONES ===
    instituciones_nombres: List[str] = []                # Lista de nombres para filtro dropdown
    instituciones_info: List[Dict[str, Any]] = []        # Datos completos para galería
    
    # === DATOS DE CIUDADES ===
    ciudades_nombres: List[str] = []                     # Lista de nombres de ciudades para filtro dropdown
    
    # === UI CONTROL - MODAL DE INSTITUCIONES ===
    is_dialog_open: bool = False                         # Control modal detalle institución
    selected_institution: Dict[str, Any] = {}           # Institución seleccionada en modal
    ciudad_filtro_instituciones: str = ""                # Filtro de ciudad para instituciones
    
    # === RESPONSIVE DESIGN ===
    is_mobile: bool = False                              # Detector de dispositivos móviles
    
    # ================================================================================
    # VARIABLES DE ESTADO - FUNCIONALIDAD AUTENTICACIÓN
    # ================================================================================
    
    # === MODAL LOGIN (desde header) ===
    show_login_dialog: bool = False                      # Control modal login en header
    login_correo: str = ""                               # Campo email del formulario
    login_password: str = ""                             # Campo contraseña del formulario
    login_error: str = ""                                # Mensaje de error de autenticación
    
    # === MENÚ MÓVIL ===
    show_mobile_menu: bool = False                       # Control menú desplegable móvil
    
    # === SESIÓN DE USUARIO ===
    logged_in_user: Optional[User] = None                # Usuario autenticado actual
    user_authenticated: bool = False                     # Flag adicional de autenticación
    redirect_url: str = ""                               # URL para redirigir post-login
    
    # ================================================================================
    # VARIABLES DE ESTADO - FUNCIONALIDAD ADMIN CRUD
    # ================================================================================
    
    # === DATOS ADMIN ===
    admin_cursos: List[Dict[str, Any]] = []              # Cursos de la institución del admin
    
    # === UI CONTROL - FORMULARIO CURSOS ===
    show_curso_dialog: bool = False                      # Control modal formulario curso
    is_editing: bool = False                             # Modo edición vs creación
    curso_a_editar: Dict[str, Any] = {}                  # Datos del curso en edición
    
    # === UI CONTROL - CONFIRMACIÓN ELIMINAR ===
    show_delete_alert: bool = False                      # Control modal confirmación
    curso_a_eliminar_id: int = -1                        # ID del curso a eliminar
    
    # === CAMPOS DEL FORMULARIO CURSO ===
    # Campos individuales para binding directo con inputs del formulario
    form_nombre: str = ""                                # Campo nombre del curso
    form_nivel: str = ""                                 # Campo nivel educativo
    form_duracion_numero: str = ""                       # Campo duración numérica
    form_duracion_unidad: str = ""                       # Campo unidad de tiempo
    form_requisitos_ingreso: str = ""                    # Campo requisitos previos
    form_lugar: str = ""                                 # Campo lugar donde se dicta el curso
    form_informacion: str = ""                           # Campo información adicional
    
    # === OPCIONES PARA DROPDOWNS ===
    # Estas opciones se cargan desde constants.py y se usan en formularios
    opciones_nivel: List[str] = CursosConstants.NIVELES                    # ["Bachillerato", "Terciario", ...]
    opciones_requisitos: List[str] = CursosConstants.REQUISITOS_INGRESO    # ["Ciclo básico", "Bachillerato", ...]
    opciones_duracion_numero: List[str] = CursosConstants.DURACIONES_NUMEROS  # ["1", "2", ..., "12"]
    opciones_duracion_unidad: List[str] = CursosConstants.DURACIONES_UNIDADES # ["meses", "años"]
    opciones_lugar: List[str] = CursosConstants.LUGARES                    # ["Virtual", "Salto", "Montevideo", ...]

    def cargar_cursos(self):
        """Carga todos los cursos desde la base de datos con cache inteligente."""
        if not self.cursos_cache_loaded:
            print("[PERFORMANCE] Cargando cursos desde DB (primera vez)")
            self.cursos_originales = obtener_cursos()
            self.cursos_cache_loaded = True
        else:
            print("[PERFORMANCE] Usando cache de cursos (navegación rápida)")
        self.aplicar_filtros()

    def aplicar_filtros(self):
        """Aplica los filtros seleccionados a los cursos."""
        cursos_filtrados = []
        
        for curso in self.cursos_originales:
            # Aplicar filtro de nivel
            if self.nivel_seleccionado and curso['nivel'] != self.nivel_seleccionado:
                continue
            
            # Aplicar filtro de requisitos
            if self.requisito_seleccionado and curso['requisitos_ingreso'] != self.requisito_seleccionado:
                continue
            
            # Aplicar filtro de institución
            if self.institucion_seleccionada and curso['institucion'] != self.institucion_seleccionada:
                continue
            
            # Aplicar filtro de lugar
            if self.lugar_seleccionado and self.lugar_seleccionado not in curso['lugar']:
                continue
            
            # Filtro de texto manual
            if self.busqueda_texto:
                texto = self.busqueda_texto.lower()
                if texto not in (curso['nombre'] or '').lower() and texto not in (curso['informacion'] or '').lower():
                    continue
            
            cursos_filtrados.append(curso)
        
        self.cursos = cursos_filtrados
        
        # Actualizar también tabla_cursos_data para compatibilidad
        self.tabla_cursos_data = [
            [
                curso['nombre'],
                curso['nivel'],
                f"{curso['duracion_numero']} {curso['duracion_unidad']}" if curso.get('duracion_numero') and curso.get('duracion_unidad') else "N/A",
                curso['requisitos_ingreso'],
                curso['institucion'],
                curso['informacion'],
                curso['lugar']
            ]
            for curso in cursos_filtrados
        ]

    def cargar_instituciones_nombres(self):
        """Carga nombres de instituciones con cache inteligente."""
        if not self.instituciones_cache_loaded:
            print("[PERFORMANCE] Cargando instituciones desde DB (primera vez)")
            self.instituciones_nombres = ["Todos"] + obtener_instituciones_nombres()
            self.instituciones_cache_loaded = True
        else:
            print("[PERFORMANCE] Usando cache de instituciones (navegación rápida)")

    def cargar_instituciones(self):
        """Carga datos completos de instituciones (solo cuando se necesiten)."""
        self.instituciones_info = obtener_instituciones()

    def cargar_instituciones_con_sedes(self, ciudad: str = None):
        """Carga instituciones con sus sedes, opcionalmente filtradas por ciudad."""
        from .database import obtener_instituciones_con_sedes_por_ciudad
        self.instituciones_info = obtener_instituciones_con_sedes_por_ciudad(ciudad)

    def cargar_ciudades_nombres(self):
        """Carga nombres de ciudades con cache inteligente."""
        if not self.ciudades_cache_loaded:
            print("[PERFORMANCE] Cargando ciudades desde DB (primera vez)")
            self.ciudades_nombres = ["Todas"] + obtener_ciudades_nombres()
            self.ciudades_cache_loaded = True
        else:
            print("[PERFORMANCE] Usando cache de ciudades (navegación rápida)")

    def cargar_datos_cursos_page(self):
        """Carga los datos iniciales de la página de cursos con optimización de cold start."""
        print("[PERFORMANCE] cargar_datos_cursos_page ejecutándose")
        
        # === PROGRESSIVE LOADING PARA COLD START ===
        # En primera carga: mostrar página inmediatamente, cargar datos en background
        if not self.cursos_cache_loaded:
            print("[PERFORMANCE] COLD START - Implementando progressive loading")
            
            # 1. Cargar instituciones primero (query rápida)
            self.cargar_instituciones_nombres()
            
            # 2. Cargar ciudades (query rápida)
            self.cargar_ciudades_nombres()
            
            # 3. Inicializar con estado vacío para mostrar skeleton
            self.cursos = []
            self.cursos_originales = []
            
            # 4. Cargar cursos en background (query pesada optimizada)
            self.cargar_cursos()
            
            print(f"[PERFORMANCE] COLD START completado - Progressive loading aplicado")
        else:
            print("[PERFORMANCE] CACHE HIT - Carga instantánea")
            # Navegaciones subsecuentes: usar cache (instantáneo)
            self.cargar_cursos()
            self.cargar_instituciones_nombres()
            self.cargar_ciudades_nombres()
        
        print(f"[PERFORMANCE] Datos cargados - Cursos: {len(self.cursos_originales)}, Filtrados: {len(self.cursos)}")

    def cargar_datos_instituciones_page(self):
        """Carga los datos iniciales de la página de instituciones."""
        print("[PERFORMANCE] cargar_datos_instituciones_page ejecutándose")
        
        # Cargar ciudades para el filtro
        self.cargar_ciudades_nombres()
        
        # Cargar instituciones con sedes (sin filtro inicial)
        self.cargar_instituciones_con_sedes()
        
        print(f"[PERFORMANCE] Datos de instituciones cargados - Instituciones: {len(self.instituciones_info)}")

    def actualizar_nivel_seleccionado(self, nivel: str):
        self.nivel_seleccionado = "" if nivel == "Todos" else nivel
        self.aplicar_filtros()

    def actualizar_requisito_seleccionado(self, requisito: str):
        self.requisito_seleccionado = "" if requisito == "Todos" else requisito
        self.aplicar_filtros()

    def actualizar_duracion_seleccionada(self, duracion: str):
        self.duracion_seleccionada = "" if duracion == "Todos" else duracion
        self.aplicar_filtros()

    def actualizar_institución_seleccionada(self, institucion: str):
        self.institucion_seleccionada = "" if institucion == "Todos" else institucion
        self.aplicar_filtros()

    def actualizar_lugar_seleccionado(self, lugar: str):
        self.lugar_seleccionado = "" if lugar == "Todas" else lugar
        self.aplicar_filtros()

    def actualizar_busqueda_texto(self, texto: str):
        self.busqueda_texto = texto
        self.aplicar_filtros()

    def limpiar_filtros(self):
        """Limpia todos los filtros seleccionados sin recargar datos (usa cache)."""
        print("[PERFORMANCE] Limpiando filtros (sin recargar DB)")
        self.nivel_seleccionado = ""
        self.requisito_seleccionado = ""
        self.institucion_seleccionada = ""
        self.lugar_seleccionado = ""
        self.busqueda_texto = "" # Limpiar texto de búsqueda
        self.aplicar_filtros()
        
    def forzar_recarga_cache(self):
        """Fuerza la recarga del cache (útil para admin después de modificar datos)."""
        print("[PERFORMANCE] Forzando recarga de cache")
        self.cursos_cache_loaded = False
        self.instituciones_cache_loaded = False
        self.cargar_cursos()
        self.cargar_instituciones_nombres()

    def open_institution_dialog(self, institution: dict):
        self.is_dialog_open = True
        self.selected_institution = institution

    def set_dialog_open(self, is_open: bool):
        self.is_dialog_open = is_open

    def go_to_institution_courses(self):
        self.institucion_seleccionada = self.selected_institution.get("nombre", "")
        return rx.redirect("/cursos")

    def actualizar_filtro_ciudad_instituciones(self, ciudad: str):
        """Actualiza el filtro de ciudad para instituciones y recarga los datos."""
        self.ciudad_filtro_instituciones = "" if ciudad == "Todas" else ciudad
        if self.ciudad_filtro_instituciones:
            self.cargar_instituciones_con_sedes(self.ciudad_filtro_instituciones)
        else:
            self.cargar_instituciones_con_sedes()  # Sin filtro

    def toggle_login_dialog(self):
        self.show_login_dialog = not self.show_login_dialog
        self.login_error = ""
        self.login_correo = ""
        self.login_password = ""
    
    def toggle_mobile_menu(self):
        """Alterna la visibilidad del menú móvil."""
        self.show_mobile_menu = not self.show_mobile_menu
    
    def close_mobile_menu(self):
        """Cierra el menú móvil."""
        self.show_mobile_menu = False

    def set_show_login_dialog(self, show: bool):
        self.show_login_dialog = show

    def set_login_correo(self, value: str):
        self.login_correo = value

    def set_login_password(self, value: str):
        self.login_password = value

    def handle_login(self):
        self.login_error = ""
        usuario_db = obtener_usuario_por_correo(self.login_correo)

        if not usuario_db:
            self.login_error = "El correo no se encuentra registrado."
            return
        
        if bcrypt.checkpw(self.login_password.encode('utf-8'), usuario_db.password_hash.encode('utf-8')):
            self.logged_in_user = User(
                id=usuario_db.id,
                correo=usuario_db.correo,
                institucion_id=usuario_db.institucion_id,
                institucion_nombre=usuario_db.institucion.nombre  # Acceso directo gracias a selectinload
            )
            self.user_authenticated = True
            self.show_login_dialog = False
            return rx.redirect("/admin")
        else:
            self.login_error = "La contraseña es incorrecta."

    def handle_login_redirect(self):
        """Maneja el login desde la página dedicada con redirección."""
        self.login_error = ""
        usuario_db = obtener_usuario_por_correo(self.login_correo)

        if not usuario_db:
            self.login_error = "El correo no se encuentra registrado."
            return

        if bcrypt.checkpw(self.login_password.encode('utf-8'), usuario_db.password_hash.encode('utf-8')):
            self.logged_in_user = User(
                id=usuario_db.id,
                correo=usuario_db.correo,
                institucion_id=usuario_db.institucion_id,
                institucion_nombre=usuario_db.institucion.nombre # Acceso directo
            )
            self.user_authenticated = True
            self.login_correo = ""
            self.login_password = ""
            self.login_error = ""
            
            redirect_target = self.redirect_url if self.redirect_url else "/admin"
            self.redirect_url = ""
            return rx.redirect(redirect_target)
        else:
            self.login_error = "La contraseña es incorrecta."

    def set_redirect_url(self, url: str):
        """Establece la URL de redirección para después del login."""
        self.redirect_url = url

    def logout(self):
        """Cierra la sesión del usuario y limpia todos los datos relacionados."""
        self.logged_in_user = None
        self.user_authenticated = False
        self.redirect_url = ""
        # Limpiar datos del admin
        self.admin_cursos = []
        self.show_curso_dialog = False
        self.is_editing = False
        self.curso_a_editar = {}
        self.show_delete_alert = False
        self.curso_a_eliminar_id = -1
        # Limpiar campos del formulario
        self.form_nombre = ""
        self.form_nivel = ""
        self.form_duracion_numero = ""
        self.form_duracion_unidad = ""
        self.form_requisitos_ingreso = ""
        self.form_lugar = ""
        self.form_informacion = ""
        return rx.redirect("/")

    def require_authentication(self):
        """Verificación estricta de autenticación para páginas protegidas."""
        # Verificar siempre, independientemente del estado de hidratación
        if self.logged_in_user is None:
            return rx.redirect("/")
        return None
    
    def is_authenticated(self) -> bool:
        """Verifica si el usuario está autenticado."""
        result = self.logged_in_user is not None and self.user_authenticated
        print(f"[DEBUG] is_authenticated: logged_in_user={self.logged_in_user}, user_authenticated={self.user_authenticated}, result={result}")
        return result

    def require_admin_access(self):
        """Guard para rutas admin - redirige a login si no está autenticado."""
        print(f"[DEBUG] require_admin_access called. is_authenticated: {self.is_authenticated()}")
        print(f"[DEBUG] logged_in_user: {self.logged_in_user}")
        print(f"[DEBUG] user_authenticated: {self.user_authenticated}")
        
        if not self.is_authenticated():
            self.set_redirect_url("/admin")
            print("[DEBUG] Redirecting to /login")
            return rx.redirect("/login")
        
        print("[DEBUG] User is authenticated, allowing access")
        return None

    def check_admin_route_access(self, path: str = "/admin"):
        """Verifica acceso a rutas admin y redirige si es necesario."""
        if not self.is_authenticated():
            self.set_redirect_url(path)
            return rx.redirect("/login")
        return None

    def set_form_nombre(self, value: str):
        self.form_nombre = value
    
    def set_form_nivel(self, value: str):
        self.form_nivel = value
        
    def set_form_duracion_numero(self, value: str):
        self.form_duracion_numero = value
        
    def set_form_duracion_unidad(self, value: str):
        self.form_duracion_unidad = value
        
    def set_form_requisitos_ingreso(self, value: str):
        self.form_requisitos_ingreso = value
        
    def set_form_lugar(self, value: str):
        self.form_lugar = value
        
    def set_form_informacion(self, value: str):
        self.form_informacion = value

    def set_curso_a_editar_field(self, field: str, value: Any):
        """Actualiza un campo del diccionario del curso a editar."""
        self.curso_a_editar[field] = value

    def cargar_cursos_admin(self):
        """Carga los cursos para el administrador logueado."""
        print(f"[DEBUG] cargar_cursos_admin llamado")
        print(f"[DEBUG] logged_in_user: {self.logged_in_user}")
        if self.logged_in_user:
            print(f"[DEBUG] Institución ID: {self.logged_in_user.institucion_id}")
            self.admin_cursos = obtener_cursos_por_institucion(self.logged_in_user.institucion_id)
            print(f"[DEBUG] Cursos cargados: {len(self.admin_cursos)}")
            for curso in self.admin_cursos:
                print(f"[DEBUG] Curso: {curso['nombre']}")
        else:
            print(f"[DEBUG] No hay usuario logueado")
            self.admin_cursos = []

    def _reset_form_fields(self):
        """Limpia los campos del formulario."""
        self.form_nombre = ""
        self.form_nivel = ""
        self.form_duracion_numero = ""
        self.form_duracion_unidad = ""
        self.form_requisitos_ingreso = ""
        self.form_lugar = ""
        self.form_informacion = ""
        self.curso_a_editar = {}
        self.is_editing = False

    def abrir_dialogo_agregar(self):
        self._reset_form_fields()
        self.show_curso_dialog = True

    def abrir_dialogo_editar(self, curso: dict):
        self.is_editing = True
        self.curso_a_editar = curso
        # Precargar formulario
        self.form_nombre = curso.get("nombre", "")
        self.form_nivel = curso.get("nivel", "")
        self.form_duracion_numero = str(curso.get("duracion_numero", ""))
        self.form_duracion_unidad = curso.get("duracion_unidad", "")
        self.form_requisitos_ingreso = curso.get("requisitos_ingreso", "")
        self.form_lugar = curso.get("lugar", "")
        self.form_informacion = curso.get("informacion", "")
        self.show_curso_dialog = True

    def cerrar_dialogo(self):
        """Cierra el diálogo del formulario y resetea los campos."""
        self.show_curso_dialog = False
        self.is_editing = False
        self._reset_form_fields()

    def guardar_curso(self):
        """Guarda un curso nuevo o modifica uno existente."""
        if not self.logged_in_user:
            return rx.window_alert("Error: No hay usuario autenticado.")

        # Construir el diccionario de datos del curso desde el formulario
        curso_data = {
            "nombre": self.form_nombre,
            "nivel": self.form_nivel,
            "duracion_numero": self.form_duracion_numero,
            "duracion_unidad": self.form_duracion_unidad,
            "requisitos_ingreso": self.form_requisitos_ingreso,
            "lugar": self.form_lugar,
            "informacion": self.form_informacion,
            "institucion_id": self.logged_in_user.institucion_id,
        }

        try:
            if self.is_editing:
                # Modificar curso existente
                curso_id = self.curso_a_editar.get("id")
                if curso_id:
                    modificar_curso(curso_id, curso_data)
                    print(f"Curso modificado con ID: {curso_id}")
                else:
                    return rx.window_alert("Error: No se encontró el ID del curso a editar.")
            else:
                # Agregar nuevo curso
                agregar_curso(curso_data)
                print("Nuevo curso agregado.")
            
            # Recargar la lista de cursos y cerrar el diálogo
            self.cargar_cursos_admin()
            self.cerrar_dialogo()

        except Exception as e:
            print(f"Error al guardar el curso: {e}")
            return rx.window_alert(f"No se pudo guardar el curso: {e}")
    
    def handle_submit_curso(self, form_data: dict):
        """Esta función parece redundante si usamos guardar_curso.
        Por ahora la dejamos pero la lógica principal estará en guardar_curso."""
        print("Manejando submit de curso:", form_data)
        if self.is_editing:
            modificar_curso(self.curso_a_editar["id"], form_data)
        else:
            agregar_curso(form_data)
        
        self.cargar_cursos_admin()
        self.show_curso_dialog = False

    def abrir_alerta_eliminar(self, curso_id: int):
        self.curso_a_eliminar_id = curso_id
        self.show_delete_alert = True

    def cerrar_alerta_eliminar(self):
        self.curso_a_eliminar_id = -1
        self.show_delete_alert = False

    def set_show_delete_alert(self, show: bool):
        """Controla la visibilidad de la alerta de eliminación."""
        self.show_delete_alert = show

    def confirmar_eliminacion(self):
        if self.curso_a_eliminar_id != -1:
            eliminar_curso(self.curso_a_eliminar_id)
            self.cargar_cursos_admin()
            self.cerrar_alerta_eliminar()

    # Funciones para manejar eventos de AG Grid
    def handle_ag_grid_edit(self, curso_data: dict):
        """Maneja el evento de edición desde AG Grid."""
        print(f"[DEBUG] AG Grid Edit evento: {curso_data}")
        self.abrir_dialogo_editar(curso_data)

    def handle_ag_grid_delete(self, curso_id: int):
        """Maneja el evento de eliminación desde AG Grid."""
        print(f"[DEBUG] AG Grid Delete evento: {curso_id}")
        self.abrir_alerta_eliminar(curso_id)

    def on_ag_grid_event(self, event_data: dict):
        """Evento genérico para manejar todas las acciones de AG Grid."""
        event_type = event_data.get("type", "")
        
        if event_type == "edit":
            curso_data = event_data.get("curso", {})
            self.abrir_dialogo_editar(curso_data)
        elif event_type == "delete":
            curso_id = event_data.get("id", -1)
            if curso_id != -1:
                self.abrir_alerta_eliminar(curso_id)
