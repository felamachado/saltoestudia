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
    
    # === CONTROL DE LIMPIEZA DE FILTROS ===
    mantener_filtro_institucion: bool = False            # Flag para mantener filtro de institución al cargar página
    mantener_filtro_lugar: bool = False                  # Flag para mantener filtro de lugar al cargar página
    
    # === DATOS DE INSTITUCIONES ===
    instituciones_nombres: List[str] = []                # Lista de nombres para filtro dropdown
    instituciones_info: List[Dict[str, Any]] = []        # Datos completos para galería
    
    # === DATOS DE CIUDADES ===
    ciudades_nombres: List[str] = []                     # Lista de nombres de ciudades para filtro dropdown
    
    # === UI CONTROL - MODAL DE INSTITUCIONES ===
    is_dialog_open: bool = False                         # Control modal detalle institución
    selected_institution: Dict[str, Any] = {}           # Institución seleccionada en modal
    selected_institution_sedes: List[Dict[str, Any]] = [] # Sedes de la institución seleccionada
    ciudad_filtro_instituciones: str = ""                # Filtro de ciudad para instituciones
    expanded_sede_id: Optional[int] = None               # ID de la sede expandida en el acordeón
    
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
    admin_sedes: List[Dict[str, Any]] = []               # Sedes de la institución del admin
    
    # === UI CONTROL - FORMULARIO CURSOS ===
    show_curso_dialog: bool = False                      # Control modal formulario curso
    is_editing: bool = False                             # Modo edición vs creación
    curso_a_editar: Dict[str, Any] = {}                  # Datos del curso en edición
    
    # === UI CONTROL - FORMULARIO SEDES ===
    show_sede_dialog: bool = False                       # Control modal formulario sede
    is_editing_sede: bool = False                        # Modo edición vs creación para sedes
    sede_a_editar: Dict[str, Any] = {}                   # Datos de la sede en edición
    
    # === UI CONTROL - CONFIRMACIÓN ELIMINAR ===
    show_delete_alert: bool = False                      # Control modal confirmación
    curso_a_eliminar_id: int = -1                        # ID del curso a eliminar
    sede_a_eliminar_id: int = -1                         # ID de la sede a eliminar
    
    # === CAMPOS DEL FORMULARIO CURSO ===
    # Campos individuales para binding directo con inputs del formulario
    form_nombre: str = ""                                # Campo nombre del curso
    form_nivel: str = ""                                 # Campo nivel educativo
    form_duracion_numero: str = ""                       # Campo duración numérica
    form_duracion_unidad: str = ""                       # Campo unidad de tiempo
    form_requisitos_ingreso: str = ""                    # Campo requisitos previos
    form_lugar: str = ""                                 # Campo lugar donde se dicta el curso
    form_informacion: str = ""                           # Campo información adicional
    # === NUEVO: soporte para selección múltiple de ciudades ===
    form_ciudades: List[str] = []                        # Lista de ciudades seleccionadas en el formulario
    form_ciudades_opciones: List[str] = []               # Opciones de ciudades válidas para la institución
    
    # === CAMPOS DEL FORMULARIO SEDE ===
    # Campos individuales para binding directo con inputs del formulario de sedes
    form_sede_direccion: str = ""                        # Campo dirección de la sede
    form_sede_telefono: str = ""                         # Campo teléfono de la sede
    form_sede_email: str = ""                            # Campo email de la sede
    form_sede_web: str = ""                              # Campo sitio web de la sede
    form_sede_ciudad: str = ""                           # Campo ciudad de la sede

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
        print(f"[DEBUG] aplicar_filtros - Filtros activos:")
        print(f"  - institucion_seleccionada: '{self.institucion_seleccionada}'")
        print(f"  - lugar_seleccionado: '{self.lugar_seleccionado}'")
        print(f"  - nivel_seleccionado: '{self.nivel_seleccionado}'")
        print(f"  - requisito_seleccionado: '{self.requisito_seleccionado}'")
        print(f"  - busqueda_texto: '{self.busqueda_texto}'")
        
        cursos_filtrados = []
        total_cursos = len(self.cursos_originales)
        filtrados_por_institucion = 0
        filtrados_por_lugar = 0
        
        for curso in self.cursos_originales:
            # Aplicar filtro de nivel
            if self.nivel_seleccionado and curso['nivel'] != self.nivel_seleccionado:
                continue
            
            # Aplicar filtro de requisitos
            if self.requisito_seleccionado and curso['requisitos_ingreso'] != self.requisito_seleccionado:
                continue
            
            # Aplicar filtro de institución
            if self.institucion_seleccionada:
                if curso['institucion'] != self.institucion_seleccionada:
                    filtrados_por_institucion += 1
                    continue
            
            # Aplicar filtro de lugar
            if self.lugar_seleccionado:
                if self.lugar_seleccionado not in curso['lugar']:
                    filtrados_por_lugar += 1
                    continue
            
            # Filtro de texto manual
            if self.busqueda_texto:
                texto = self.busqueda_texto.lower()
                if texto not in (curso['nombre'] or '').lower() and texto not in (curso['informacion'] or '').lower():
                    continue
            
            cursos_filtrados.append(curso)
        
        print(f"[DEBUG] aplicar_filtros - Resultados:")
        print(f"  - Total cursos: {total_cursos}")
        print(f"  - Filtrados por institución: {filtrados_por_institucion}")
        print(f"  - Filtrados por lugar: {filtrados_por_lugar}")
        print(f"  - Cursos finales: {len(cursos_filtrados)}")
        
        # Debug: mostrar algunos cursos para verificar nombres de instituciones
        if self.institucion_seleccionada:
            print(f"[DEBUG] aplicar_filtros - Verificando nombres de instituciones:")
            instituciones_en_cursos = set()
            for curso in self.cursos_originales[:5]:  # Solo los primeros 5
                instituciones_en_cursos.add(curso.get('institucion', 'Sin institución'))
            print(f"  - Instituciones en cursos: {instituciones_en_cursos}")
            print(f"  - Buscando: '{self.institucion_seleccionada}'")
        
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

    def cargar_sedes_como_tarjetas(self, ciudad: str = None):
        """Carga las sedes como tarjetas individuales, opcionalmente filtradas por ciudad."""
        from .database import obtener_sedes_como_tarjetas
        self.instituciones_info = obtener_sedes_como_tarjetas(ciudad)

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
        print(f"[DEBUG] cargar_datos_cursos_page - Estado inicial de filtros:")
        print(f"  - institucion_seleccionada: '{self.institucion_seleccionada}'")
        print(f"  - lugar_seleccionado: '{self.lugar_seleccionado}'")
        print(f"  - mantener_filtro_institucion: {self.mantener_filtro_institucion}")
        print(f"  - mantener_filtro_lugar: {self.mantener_filtro_lugar}")
        
        # === LIMPIAR FILTROS AL CARGAR LA PÁGINA ===
        # Limpiar filtros básicos
        self.nivel_seleccionado = ""
        self.requisito_seleccionado = ""
        self.busqueda_texto = ""
        
        # Solo limpiar institución si no se debe mantener
        if not self.mantener_filtro_institucion:
            self.institucion_seleccionada = ""
            print("[PERFORMANCE] Todos los filtros limpiados al cargar página")
        else:
            print("[PERFORMANCE] Filtros limpiados excepto institución")
            self.mantener_filtro_institucion = False  # Resetear flag para próximas cargas
        
        # Solo limpiar lugar si no se debe mantener
        if not self.mantener_filtro_lugar:
            self.lugar_seleccionado = ""
        else:
            print("[PERFORMANCE] Filtro de lugar mantenido")
            self.mantener_filtro_lugar = False  # Resetear flag para próximas cargas
        
        print(f"[DEBUG] cargar_datos_cursos_page - Estado final de filtros:")
        print(f"  - institucion_seleccionada: '{self.institucion_seleccionada}'")
        print(f"  - lugar_seleccionado: '{self.lugar_seleccionado}'")
        
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
        print("[DEBUG] cargar_datos_instituciones_page ejecutándose")
        
        # Limpiar estado del modal al cargar la página
        self.limpiar_modal_institucion()
        
        # Limpiar filtro de ciudad para mostrar todas las instituciones
        self.ciudad_filtro_instituciones = ""
        
        # Cargar ciudades para el filtro
        self.cargar_ciudades_nombres()
        print(f"[DEBUG] Ciudades cargadas: {len(self.ciudades_nombres)}")
        
        # Cargar sedes como tarjetas individuales (sin filtro inicial)
        self.cargar_sedes_como_tarjetas()
        print(f"[DEBUG] Sedes cargadas: {len(self.instituciones_info)}")
        
        # Debug: mostrar las primeras 3 sedes
        for i, sede in enumerate(self.instituciones_info[:3]):
            print(f"[DEBUG] Sede {i+1}: {sede.get('nombre', 'Sin nombre')} - {sede.get('ciudad', 'Sin ciudad')}")
        
        print(f"[DEBUG] Datos de instituciones cargados - Tarjetas de sedes: {len(self.instituciones_info)}")

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
        
        # Verificar si es una institución virtual (tiene ciudad "Virtual")
        if institution.get("ciudad") == "Virtual":
            # Crear una sede virtual especial
            sede_virtual = {
                "id": None,
                "nombre": "Cursos Virtuales",
                "direccion": "Modalidad online",
                "telefono": "N/A",
                "email": "N/A",
                "web": "N/A",
                "ciudad": "Virtual",
                "institucion_nombre": institution.get("institucion_nombre", institution.get("nombre", ""))
            }
            self.selected_institution_sedes = [sede_virtual]
        else:
            # Cargar las sedes físicas de la institución
            from .database import obtener_sedes_fisicas_por_institucion
            self.selected_institution_sedes = obtener_sedes_fisicas_por_institucion(institution.get("institucion_id", institution.get("id")))

    def set_dialog_open(self, is_open: bool):
        self.is_dialog_open = is_open
        # Si se está cerrando el modal, limpiar también la institución seleccionada
        if not is_open:
            self.selected_institution = {}
    
    def limpiar_modal_institucion(self):
        """Limpia completamente el estado del modal de institución."""
        self.is_dialog_open = False
        self.selected_institution = {}
        self.selected_institution_sedes = []
        self.expanded_sede_id = None  # Limpiar también la sede expandida

    def go_to_institution_courses(self):
        # Usar el nombre de la institución, no el de la sede
        self.institucion_seleccionada = self.selected_institution.get("institucion_nombre", "")
        # Marcar que se debe mantener el filtro de institución
        self.mantener_filtro_institucion = True
        # Cerrar el modal antes de redirigir
        self.limpiar_modal_institucion()
        return rx.redirect("/cursos")
    
    def go_to_sede_courses(self, sede: dict):
        """Navega a la página de cursos con filtros específicos de sede."""
        print(f"[DEBUG] go_to_sede_courses - Datos de sede recibidos: {sede}")
        
        # Obtener el nombre de la institución
        # Si es una sede virtual, usar el nombre de la institución desde la sede
        if sede.get("ciudad") == "Virtual":
            institucion_nombre = sede.get("institucion_nombre", "")
        else:
            # Usar siempre el nombre de la institución seleccionada
            institucion_nombre = self.selected_institution.get("nombre", "")
        
        # Establecer filtros específicos de la sede
        self.institucion_seleccionada = institucion_nombre
        self.lugar_seleccionado = sede.get("ciudad", "")
        
        # Marcar que se deben mantener los filtros de institución y lugar
        self.mantener_filtro_institucion = True
        self.mantener_filtro_lugar = True
        
        print(f"[DEBUG] go_to_sede_courses - Filtros establecidos:")
        print(f"  - Institución: '{self.institucion_seleccionada}'")
        print(f"  - Lugar: '{self.lugar_seleccionado}'")
        print(f"  - mantener_filtro_institucion: {self.mantener_filtro_institucion}")
        print(f"  - mantener_filtro_lugar: {self.mantener_filtro_lugar}")
        
        # Cerrar el modal antes de redirigir
        self.limpiar_modal_institucion()
        return rx.redirect("/cursos")

    def actualizar_filtro_ciudad_instituciones(self, ciudad: str):
        """Actualiza el filtro de ciudad para instituciones y recarga los datos."""
        self.ciudad_filtro_instituciones = ciudad
        if not ciudad or ciudad == "Todas":
            self.cargar_sedes_como_tarjetas()  # Sin filtro
        elif ciudad == "Virtual":
            from .database import obtener_instituciones_con_cursos_virtuales
            # Obtener instituciones que tienen cursos virtuales
            self.instituciones_info = obtener_instituciones_con_cursos_virtuales()
        else:
            self.cargar_sedes_como_tarjetas(ciudad)
    
    def toggle_sede_acordeon(self, sede_id: int):
        """Alterna la expansión de una sede en el acordeón."""
        if self.expanded_sede_id == sede_id:
            self.expanded_sede_id = None  # Cerrar si ya está abierta
        else:
            self.expanded_sede_id = sede_id  # Abrir esta sede

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
        self.admin_sedes = []
        self.show_curso_dialog = False
        self.is_editing = False
        self.curso_a_editar = {}
        self.show_sede_dialog = False
        self.is_editing_sede = False
        self.sede_a_editar = {}
        self.show_delete_alert = False
        self.curso_a_eliminar_id = -1
        self.sede_a_eliminar_id = -1
        # Limpiar campos del formulario de cursos
        self.form_nombre = ""
        self.form_nivel = ""
        self.form_duracion_numero = ""
        self.form_duracion_unidad = ""
        self.form_requisitos_ingreso = ""
        self.form_lugar = ""
        self.form_informacion = ""
        self.form_ciudades = [] # Limpiar ciudades
        self.form_ciudades_opciones = [] # Limpiar ciudades válidas
        # Limpiar campos del formulario de sedes
        self.form_sede_direccion = ""
        self.form_sede_telefono = ""
        self.form_sede_email = ""
        self.form_sede_web = ""
        self.form_sede_ciudad = ""
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

    def set_form_ciudades(self, value):
        # value puede venir como lista o string (de un select múltiple)
        if isinstance(value, str):
            # Reflex puede enviar un string separado por comas
            self.form_ciudades = value.split(",") if value else []
        else:
            self.form_ciudades = value or []

    def toggle_ciudad(self, ciudad: str, checked: bool):
        if checked:
            if ciudad not in self.form_ciudades:
                self.form_ciudades = self.form_ciudades + [ciudad]
        else:
            self.form_ciudades = [c for c in self.form_ciudades if c != ciudad]

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
        self.form_ciudades = []
        self.form_ciudades_opciones = []
        self.curso_a_editar = {}
        self.is_editing = False

    def abrir_dialogo_agregar(self):
        self._reset_form_fields()
        self.form_ciudades = []
        # Cargar ciudades válidas para la institución
        self.form_ciudades_opciones = []
        if self.logged_in_user:
            # Buscar la institución y sus sedes
            for inst in self.instituciones_info:
                if inst["id"] == self.logged_in_user.institucion_id:
                    self.form_ciudades_opciones = [sede["ciudad"] for sede in inst.get("sedes", [])]
                    break
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
        # Precargar ciudades (parsear string separado por coma a lista)
        lugar_str = curso.get("lugar", "")
        self.form_ciudades = [c.strip() for c in lugar_str.split(",") if c.strip()] if lugar_str else []
        # Cargar ciudades válidas para la institución
        self.form_ciudades_opciones = []
        if self.logged_in_user:
            for inst in self.instituciones_info:
                if inst["id"] == self.logged_in_user.institucion_id:
                    self.form_ciudades_opciones = [sede["ciudad"] for sede in inst.get("sedes", [])]
                    break
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
            # NUEVO: enviar ciudades seleccionadas
            "ciudades": self.form_ciudades,
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
        elif self.sede_a_eliminar_id != -1:
            from .database import eliminar_sede
            eliminar_sede(self.sede_a_eliminar_id)
            self.cargar_sedes_admin()
            self.cerrar_alerta_eliminar_sede()

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

    # ================================================================================
    # FUNCIONES DE GESTIÓN DE SEDES
    # ================================================================================

    def cargar_sedes_admin(self):
        """Carga las sedes para el administrador logueado."""
        print(f"[DEBUG] cargar_sedes_admin llamado")
        print(f"[DEBUG] logged_in_user: {self.logged_in_user}")
        if self.logged_in_user:
            print(f"[DEBUG] Institución ID: {self.logged_in_user.institucion_id}")
            from .database import obtener_sedes_fisicas_por_institucion
            self.admin_sedes = obtener_sedes_fisicas_por_institucion(self.logged_in_user.institucion_id)
            print(f"[DEBUG] Sedes cargadas: {len(self.admin_sedes)}")
            for sede in self.admin_sedes:
                print(f"[DEBUG] Sede: {sede['nombre']}")
        else:
            print(f"[DEBUG] No hay usuario logueado")
            self.admin_sedes = []

    def _reset_sede_form_fields(self):
        """Limpia los campos del formulario de sede."""
        self.form_sede_direccion = ""
        self.form_sede_telefono = ""
        self.form_sede_email = ""
        self.form_sede_web = ""
        self.form_sede_ciudad = ""
        self.sede_a_editar = {}
        self.is_editing_sede = False

    def abrir_dialogo_agregar_sede(self):
        """Abre el diálogo para agregar una nueva sede."""
        self._reset_sede_form_fields()
        self.show_sede_dialog = True

    def abrir_dialogo_editar_sede(self, sede: dict):
        """Abre el diálogo para editar una sede existente."""
        self.is_editing_sede = True
        self.sede_a_editar = sede
        # Precargar formulario
        self.form_sede_direccion = sede.get("direccion", "")
        self.form_sede_telefono = sede.get("telefono", "")
        self.form_sede_email = sede.get("email", "")
        self.form_sede_web = sede.get("web", "")
        self.form_sede_ciudad = sede.get("ciudad", "")
        self.show_sede_dialog = True

    def cerrar_dialogo_sede(self):
        """Cierra el diálogo del formulario de sede y resetea los campos."""
        self.show_sede_dialog = False
        self.is_editing_sede = False
        self._reset_sede_form_fields()

    def guardar_sede(self):
        """Guarda una sede nueva o modifica una existente."""
        if not self.logged_in_user:
            return rx.window_alert("Error: No hay usuario autenticado.")

        # Construir el diccionario de datos de la sede desde el formulario
        sede_data = {
            "direccion": self.form_sede_direccion,
            "telefono": self.form_sede_telefono,
            "email": self.form_sede_email,
            "web": self.form_sede_web,
            "ciudad": self.form_sede_ciudad,
            "institucion_id": self.logged_in_user.institucion_id,
        }

        try:
            if self.is_editing_sede:
                # Modificar sede existente
                sede_id = self.sede_a_editar.get("id")
                if sede_id:
                    from .database import modificar_sede
                    modificar_sede(sede_id, sede_data)
                    print(f"Sede modificada con ID: {sede_id}")
                else:
                    return rx.window_alert("Error: No se encontró el ID de la sede a editar.")
            else:
                # Agregar nueva sede
                from .database import agregar_sede
                agregar_sede(sede_data)
                print("Nueva sede agregada.")
            
            # Recargar la lista de sedes y cerrar el diálogo
            self.cargar_sedes_admin()
            self.cerrar_dialogo_sede()

        except Exception as e:
            print(f"Error al guardar la sede: {e}")
            return rx.window_alert(f"No se pudo guardar la sede: {e}")

    def abrir_alerta_eliminar_sede(self, sede_id: int):
        """Abre la alerta de confirmación para eliminar una sede."""
        self.sede_a_eliminar_id = sede_id
        self.show_delete_alert = True

    def cerrar_alerta_eliminar_sede(self):
        """Cierra la alerta de eliminación de sede."""
        self.sede_a_eliminar_id = -1
        self.show_delete_alert = False

    def confirmar_eliminacion_sede(self):
        """Confirma la eliminación de una sede."""
        if self.sede_a_eliminar_id != -1:
            from .database import eliminar_sede
            eliminar_sede(self.sede_a_eliminar_id)
            self.cargar_sedes_admin()
            self.cerrar_alerta_eliminar_sede()

    # Setters para los campos del formulario de sede
    def set_form_sede_direccion(self, value: str):
        self.form_sede_direccion = value
        
    def set_form_sede_telefono(self, value: str):
        self.form_sede_telefono = value
        
    def set_form_sede_email(self, value: str):
        self.form_sede_email = value
        
    def set_form_sede_web(self, value: str):
        self.form_sede_web = value
        
    def set_form_sede_ciudad(self, value: str):
        self.form_sede_ciudad = value
