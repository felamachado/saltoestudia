# saltoestudia/state.py

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
)
from .models import Usuario
from .constants import CursosConstants

class User(rx.Base):
    """Modelo de usuario seguro para el estado de Reflex."""
    id: int
    correo: str
    institucion_id: int
    institucion_nombre: str

class State(rx.State):
    cursos: List[Dict[str, Any]] = []
    cursos_originales: List[Dict[str, Any]] = []  # Nueva variable para almacenar todos los cursos
    instituciones_nombres : List[str] = []
    nivel_seleccionado: str = ""
    duracion_seleccionada: str = ""
    requisito_seleccionado: str = ""
    institucion_seleccionada: str = ""
    tabla_cursos_data: List[List[Any]] = []

    instituciones_info: List[Dict[str, Any]] = []
    is_dialog_open: bool = False
    selected_institution: Dict[str, Any] = {}

    # NUEVO: Variable para la lógica responsiva. Soluciona el AttributeError.
    is_mobile: bool = False

    show_login_dialog: bool = False
    login_correo: str = ""
    login_password: str = ""
    login_error: str = ""
    logged_in_user: Optional[User] = None

    # Variables para manejo de redirección después del login
    redirect_url: str = ""
    user_authenticated: bool = False

    def cargar_cursos(self):
        """Carga todos los cursos desde la base de datos."""
        self.cursos_originales = obtener_cursos()
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
                curso['informacion']
            ]
            for curso in cursos_filtrados
        ]

    def cargar_instituciones_nombres(self):
        self.instituciones_nombres = ["Todos"] + obtener_instituciones_nombres()

    def cargar_instituciones(self):
        self.instituciones_info = obtener_instituciones()

    def cargar_datos_cursos_page(self):
        """Carga los datos iniciales de la página de cursos."""
        self.cargar_cursos()
        self.cargar_instituciones_nombres()

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

    def limpiar_filtros(self):
        """Limpia todos los filtros seleccionados y recarga los datos."""
        self.nivel_seleccionado = ""
        self.requisito_seleccionado = ""
        self.institucion_seleccionada = ""
        self.aplicar_filtros()

    def open_institution_dialog(self, institution: dict):
        self.is_dialog_open = True
        self.selected_institution = institution

    def set_dialog_open(self, is_open: bool):
        self.is_dialog_open = is_open

    def go_to_institution_courses(self):
        self.institucion_seleccionada = self.selected_institution.get("nombre", "")
        return rx.redirect("/cursos")

    def toggle_login_dialog(self):
        self.show_login_dialog = not self.show_login_dialog
        self.login_error = ""
        self.login_correo = ""
        self.login_password = ""

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

    admin_cursos: List[Dict[str, Any]] = []
    show_curso_dialog: bool = False
    is_editing: bool = False
    curso_a_editar: Dict[str, Any] = {}
    show_delete_alert: bool = False
    curso_a_eliminar_id: int = -1

    # Campos individuales del formulario para edición
    form_nombre: str = ""
    form_nivel: str = ""
    form_duracion_numero: str = ""
    form_duracion_unidad: str = ""
    form_requisitos_ingreso: str = ""
    form_informacion: str = ""

    # Usar constantes hardcodeadas
    opciones_nivel: List[str] = CursosConstants.NIVELES
    opciones_requisitos: List[str] = CursosConstants.REQUISITOS_INGRESO
    opciones_duracion_numero: List[str] = CursosConstants.DURACIONES_NUMEROS
    opciones_duracion_unidad: List[str] = CursosConstants.DURACIONES_UNIDADES

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
