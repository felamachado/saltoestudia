# saltoestudia/pages/admin.py

import reflex as rx
from ..state import State
from ..constants import CursosConstants
from .. import theme
from ..theme import ButtonStyle, ComponentStyle, create_course_table_header, create_course_table_cell, create_custom_dropdown_css
from typing import Dict, Any

def admin_layout(*content) -> rx.Component:
    """Layout simple para la página de administración."""
    return rx.vstack(
        rx.hstack(
            rx.heading(
                "Panel de Administración",
                color=theme.Color.GRAY_900,
                font_family=theme.Typography.FONT_FAMILY,
            ),
            rx.spacer(),
            rx.button(
                "Cerrar Sesión", 
                on_click=State.logout,
                **ButtonStyle.primary(),
                font_family=theme.Typography.FONT_FAMILY,
            ),
            width="100%",
            padding="1em 2em",
            bg=theme.Color.GRAY_300,
            align_items="center"
        ),
        rx.box(
            *content,
            padding="2em",
            width="100%",
            flex_grow="1",
        ),
        min_height="100vh",
        width="100%",
        align_items="stretch",
        bg=theme.Color.GRAY_100,
    )

def curso_form_dialog() -> rx.Component:
    """Diálogo que contiene el formulario para agregar o editar un curso."""
    return rx.cond(
        State.show_curso_dialog,
        rx.box(
            rx.box(
                rx.vstack(
                    # Header del diálogo
                    rx.hstack(
                        rx.heading(
                            rx.cond(
                                State.is_editing,
                                "Editar Curso",
                                "Agregar Nuevo Curso"
                            ),
                            size="5",
                            font_family=theme.Typography.FONT_FAMILY,
                            font_weight=theme.Typography.FONT_WEIGHTS["semibold"],
                            color=theme.Color.GRAY_900,
                        ),
                        align_items="center",
                        spacing="3",
                        width="100%",
                    ),
                    
                    rx.divider(border_color=theme.Color.GRAY_500),
                    
                    # Contenido del formulario
                    rx.vstack(
                        # Campo Nombre
                        rx.vstack(
                            rx.text("Nombre del curso", **ComponentStyle.FORM_LABEL),
                            rx.input(
                                value=State.form_nombre,
                                on_change=State.set_form_nombre,
                                placeholder="Ej: Licenciatura en Informática",
                                **ComponentStyle.FORM_INPUT,
                            ),
                            align_items="start", width="100%",
                        ),
                        
                        # Campo Nivel
                        rx.vstack(
                            rx.text("Nivel", **ComponentStyle.FORM_LABEL),
                            rx.select(
                                State.opciones_nivel,
                                value=State.form_nivel,
                                on_change=State.set_form_nivel,
                                placeholder="Seleccionar nivel",
                                **ComponentStyle.FORM_SELECT,
                            ),
                            align_items="start", width="100%",
                        ),
                        
                        # Campo Duración (Número y Unidad)
                        rx.hstack(
                            rx.vstack(
                                rx.text("Duración", **ComponentStyle.FORM_LABEL),
                                rx.select(
                                    State.opciones_duracion_numero,
                                    value=State.form_duracion_numero,
                                    on_change=State.set_form_duracion_numero,
                                    placeholder="Seleccionar",
                                    **ComponentStyle.FORM_SELECT,
                                ),
                                align_items="start", width="50%",
                            ),
                            rx.vstack(
                                rx.text("Unidad", **ComponentStyle.FORM_LABEL, opacity=0), # Placeholder for alignment
                                rx.select(
                                    State.opciones_duracion_unidad,
                                    value=State.form_duracion_unidad,
                                    on_change=State.set_form_duracion_unidad,
                                    placeholder="Seleccionar",
                                    **ComponentStyle.FORM_SELECT,
                                ),
                                align_items="start", width="50%",
                            ),
                            spacing="3",
                            width="100%",
                        ),
                        
                        # Campo Requisitos
                        rx.vstack(
                            rx.text("Requisitos de Ingreso", **ComponentStyle.FORM_LABEL),
                            rx.select(
                                State.opciones_requisitos,
                                value=State.form_requisitos_ingreso,
                                on_change=State.set_form_requisitos_ingreso,
                                placeholder="Seleccionar requisitos",
                                **ComponentStyle.FORM_SELECT,
                            ),
                            align_items="start", width="100%",
                        ),
                        
                        # Campo Información (Área de texto)
                        rx.vstack(
                            rx.text("Información Adicional", **ComponentStyle.FORM_LABEL),
                            rx.text_area(
                                value=State.form_informacion,
                                on_change=State.set_form_informacion,
                                placeholder="Añade un enlace, descripción o cualquier detalle relevante.",
                                **ComponentStyle.FORM_INPUT,
                                resize="vertical",
                            ),
                            align_items="start", width="100%",
                        ),
                        
                        spacing="4",
                        padding_y="1em",
                        width="100%",
                    ),
                    
                    rx.divider(border_color=theme.Color.GRAY_500),
                    
                    # Botones de acción
                    rx.hstack(
                        rx.button(
                            "Cancelar",
                            on_click=State.cerrar_dialogo,
                            **ButtonStyle.secondary(),
                            font_family=theme.Typography.FONT_FAMILY,
                        ),
                        rx.button(
                            "Guardar Curso",
                            on_click=State.guardar_curso,
                            **ButtonStyle.primary(),
                            font_family=theme.Typography.FONT_FAMILY,
                        ),
                        spacing="3",
                        justify="end",
                        width="100%",
                    ),
                    
                    spacing="4",
                    width="100%",
                ),
                **ComponentStyle.MODAL,
                padding="24px",
                max_width="500px",
                width="90%",
            ),
            position="fixed",
            top="0",
            left="0",
            width="100vw",
            height="100vh",
            bg="rgba(0,0,0,0.6)",
            display="flex",
            align_items="center",
            justify_content="center",
            z_index="1000",
        )
    )

def delete_alert_dialog() -> rx.Component:
    """Alerta de confirmación para eliminar un curso."""
    return rx.cond(
        State.show_delete_alert,
        rx.box(
            rx.box(
                rx.vstack(
                    # Header del diálogo
                    rx.hstack(
                            rx.icon(
        tag="alarm_clock", 
                            size=24, 
                            color=theme.Color.DANGER,
                        ),
                        rx.heading(
                            "Confirmar eliminación",
                            size="4",
                            font_family=theme.Typography.FONT_FAMILY,
                            font_weight=theme.Typography.FONT_WEIGHTS["semibold"],
                            color=theme.Color.GRAY_900,
                        ),
                        align_items="center",
                        spacing="3",
                        width="100%",
                    ),
                    
                    rx.divider(border_color=theme.Color.GRAY_500),
                    
                    # Contenido del mensaje
                    rx.text(
                        "¿Estás seguro de que deseas eliminar este curso? Esta acción no se puede deshacer.",
                        color=theme.Color.GRAY_900,
                        font_family=theme.Typography.FONT_FAMILY,
                        text_align="center",
                        line_height="1.5",
                    ),
                    
                    rx.divider(border_color=theme.Color.GRAY_500),
                    
                    # Botones de acción
                    rx.hstack(
                        rx.button(
                            "Cancelar",
                            on_click=State.cerrar_alerta_eliminar,
                            **ButtonStyle.secondary(),
                            font_family=theme.Typography.FONT_FAMILY,
                            font_weight=theme.Typography.FONT_WEIGHTS["medium"],
                        ),
                        rx.button(
                            "Eliminar",
                            on_click=State.confirmar_eliminacion,
                            **ButtonStyle.danger(),
                            font_family=theme.Typography.FONT_FAMILY,
                            font_weight=theme.Typography.FONT_WEIGHTS["medium"],
                        ),
                        spacing="3",
                        justify="end",
                        width="100%",
                    ),
                    
                    spacing="4",
                    width="100%",
                ),
                **ComponentStyle.MODAL,
                padding="24px",
                max_width="400px",
                width="90%",
            ),
            position="fixed",
            top="0",
            left="0",
            width="100vw",
            height="100vh",
            bg="rgba(0,0,0,0.6)",
            display="flex",
            align_items="center",
            justify_content="center",
            z_index="1000",
        )
    )

def unauthorized_access_page() -> rx.Component:
    """Página que se muestra cuando se intenta acceder al admin sin estar logueado."""
    return rx.vstack(
        rx.box(
            rx.vstack(
                rx.icon(
                    tag="lock",
                    size=64,
                    color=theme.Color.DANGER,
                    margin_bottom="1em",
                ),
                rx.heading(
                    "Acceso Restringido",
                    size="8",
                    color=theme.Color.GRAY_900,
                    font_family=theme.Typography.FONT_FAMILY,
                    font_weight=theme.Typography.FONT_WEIGHTS["bold"],
                    text_align="center",
                    margin_bottom="0.5em",
                ),
                rx.text(
                    "Necesitas iniciar sesión como administrador para acceder a esta página.",
                    color=theme.Color.GRAY_700,
                    font_family=theme.Typography.FONT_FAMILY,
                    text_align="center",
                    font_size="4",
                    margin_bottom="2em",
                ),
                rx.hstack(
                    rx.button(
                        "Ir al Inicio",
                        on_click=rx.redirect("/"),
                        **ButtonStyle.primary(),
                        font_family=theme.Typography.FONT_FAMILY,
                    ),
                    rx.button(
                        "Ver Cursos",
                        on_click=rx.redirect("/cursos"),
                        **ButtonStyle.secondary(),
                        font_family=theme.Typography.FONT_FAMILY,
                    ),
                    spacing="4",
                    justify="center",
                ),
                spacing="4",
                align_items="center",
                padding="3em",
            ),
            bg=theme.Color.DARK_CARD,
            border=f"1px solid {theme.Color.GRAY_500}",
            border_radius="12px",
            max_width="500px",
            width="90%",
        ),
        min_height="100vh",
        width="100%",
        justify_content="center",
        align_items="center",
        bg=theme.Color.GRAY_100,
        padding="2em",
    )

def admin_action_buttons(curso: Dict[str, Any]) -> rx.Component:
    """Componente para los botones de acción de la fila del curso."""
    return rx.hstack(
        rx.button(
            "Editar", 
            on_click=lambda: State.abrir_dialogo_editar(curso),
            **ButtonStyle.secondary(),
            font_family=theme.Typography.FONT_FAMILY,
        ),
        rx.button(
            "Eliminar", 
            on_click=lambda: State.abrir_alerta_eliminar(curso["id"]),
            **ButtonStyle.danger(),
            font_family=theme.Typography.FONT_FAMILY,
        ),
        spacing="2"
    )

def render_curso_row(curso: Dict[str, Any]) -> rx.Component:
    """Renderiza una fila de la tabla de cursos con sus botones de acción."""
    return rx.table.row(
        create_course_table_cell(curso["nombre"]),
        create_course_table_cell(curso["nivel"]),
        create_course_table_cell(
            rx.cond(
                curso["duracion_numero"],
                f"{curso['duracion_numero']} {curso['duracion_unidad']}",
                "N/A"
            )
        ),
        create_course_table_cell(curso["requisitos_ingreso"]),
        create_course_table_cell(
            rx.cond(
                curso["informacion"],
                curso["informacion"],
                "N/A"
            )
        ),
        create_course_table_cell(admin_action_buttons(curso)),
        **ComponentStyle.COURSE_TABLE_ROW_HOVER,
    )

@rx.page(route="/admin", on_load=[State.cargar_cursos_admin])
def admin_page() -> rx.Component:
    """Página de administración para usuarios logueados."""
    # Verificación de autenticación simplificada
    return rx.cond(
        State.logged_in_user,  # Verificación directa más simple
        # Usuario autenticado - mostrar contenido admin
        admin_layout(
            create_custom_dropdown_css(),
            rx.vstack(
                rx.hstack(
                    rx.vstack(
                        rx.heading(
                            "Gestión de Cursos", 
                            size="9",
                            color=theme.Color.BLUE_300,
                            font_family=theme.Typography.FONT_FAMILY,
                            font_weight=theme.Typography.FONT_WEIGHTS["bold"],
                        ),
                        rx.cond(
                            State.logged_in_user,
                            rx.text(
                                f"Institución: {State.logged_in_user.institucion_nombre}",
                                color=theme.Color.GRAY_900,
                                font_family=theme.Typography.FONT_FAMILY,
                            ),
                            rx.text(
                                "Cargando...",
                                color=theme.Color.GRAY_700,
                                font_family=theme.Typography.FONT_FAMILY,
                            )
                        ),
                        align_items="start",
                    ),
                    rx.spacer(),
                    rx.button(
                        "Agregar Nuevo Curso", 
                        on_click=State.abrir_dialogo_agregar,
                        **ButtonStyle.primary(),
                        font_family=theme.Typography.FONT_FAMILY,
                    ),
                    align_items="end",
                    width="100%",
                    margin_bottom="2em",
                ),
                
                rx.cond(
                    State.admin_cursos,
                    # Tabla tradicional para administración de cursos (con botones funcionales)
                    rx.table.root(
                        rx.table.header(
                            create_course_table_header([
                                "Nombre", "Nivel", "Duración", "Requisitos", "Información", "Acciones"
                            ])
                        ),
                        rx.table.body(
                            rx.foreach(State.admin_cursos, render_curso_row)
                        ),
                        **ComponentStyle.COURSE_TABLE,
                    ),
                    # Mostrar mensaje cuando no hay cursos
                    rx.box(
                        rx.text(
                            "No hay cursos registrados para esta institución.",
                            color=theme.Color.GRAY_700,
                            font_family=theme.Typography.FONT_FAMILY,
                            text_align="center",
                            font_size="4",
                        ),
                        padding="4em",
                        bg=theme.Color.DARK_CARD,
                        border=f"1px solid {theme.Color.GRAY_500}",
                        border_radius="8px",
                    )
                ),

                delete_alert_dialog(),
                curso_form_dialog(),
                spacing="0",
                width="100%",
                align_items="stretch",
            )
        ),
        # Usuario no autenticado - mostrar página de redirección
        redirect_to_login_component()
    )

def redirect_to_login_component() -> rx.Component:
    """Componente que redirige automáticamente al login."""
    return rx.vstack(
        rx.script(
            """
            // Redirigir inmediatamente al login
            window.location.href = '/login';
            """,
        ),
        rx.box(
            rx.text(
                "Redirigiendo al login...",
                color=theme.Color.GRAY_700,
                font_family=theme.Typography.FONT_FAMILY,
                text_align="center",
            ),
            padding="2em",
        ),
        min_height="100vh",
        width="100%",
        justify_content="center",
        align_items="center",
        bg=theme.Color.GRAY_100,
    )
