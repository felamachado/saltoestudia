# saltoestudia/pages/admin_sedes.py

import reflex as rx
from ..state import State
from ..constants import CursosConstants
from .. import theme
from ..theme import ButtonStyle, ComponentStyle, create_custom_dropdown_css
from typing import Dict, Any

def sede_form_dialog() -> rx.Component:
    """Diálogo que contiene el formulario para agregar o editar una sede."""
    return rx.cond(
        State.show_sede_dialog,
        rx.box(
            rx.box(
                rx.vstack(
                    # Header del diálogo
                    rx.hstack(
                        rx.heading(
                            rx.cond(
                                State.is_editing_sede,
                                "Editar Sede",
                                "Agregar Nueva Sede"
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
                        # Campo Dirección
                        rx.vstack(
                            rx.text("Dirección", **ComponentStyle.FORM_LABEL),
                            rx.input(
                                value=State.form_sede_direccion,
                                on_change=State.set_form_sede_direccion,
                                placeholder="Ej: Rivera 1350",
                                **ComponentStyle.FORM_INPUT,
                            ),
                            align_items="start", width="100%",
                        ),
                        
                        # Campo Ciudad
                        rx.vstack(
                            rx.text("Ciudad", **ComponentStyle.FORM_LABEL),
                            rx.select(
                                State.ciudades_nombres,
                                value=State.form_sede_ciudad,
                                on_change=State.set_form_sede_ciudad,
                                placeholder="Seleccionar ciudad",
                                **ComponentStyle.FORM_SELECT,
                            ),
                            align_items="start", width="100%",
                        ),
                        
                        # Campo Teléfono
                        rx.vstack(
                            rx.text("Teléfono", **ComponentStyle.FORM_LABEL),
                            rx.input(
                                value=State.form_sede_telefono,
                                on_change=State.set_form_sede_telefono,
                                placeholder="Ej: 47334816",
                                **ComponentStyle.FORM_INPUT,
                            ),
                            align_items="start", width="100%",
                        ),
                        
                        # Campo Email
                        rx.vstack(
                            rx.text("Email", **ComponentStyle.FORM_LABEL),
                            rx.input(
                                value=State.form_sede_email,
                                on_change=State.set_form_sede_email,
                                placeholder="Ej: comunicacion@institucion.edu.uy",
                                **ComponentStyle.FORM_INPUT,
                            ),
                            align_items="start", width="100%",
                        ),
                        
                        # Campo Sitio Web
                        rx.vstack(
                            rx.text("Sitio Web", **ComponentStyle.FORM_LABEL),
                            rx.input(
                                value=State.form_sede_web,
                                on_change=State.set_form_sede_web,
                                placeholder="Ej: https://www.institucion.edu.uy",
                                **ComponentStyle.FORM_INPUT,
                            ),
                            align_items="start", width="100%",
                        ),
                        
                        spacing="4",
                        width="100%",
                    ),
                    
                    rx.divider(border_color=theme.Color.GRAY_500),
                    
                    # Botones de acción
                    rx.hstack(
                        rx.button(
                            "Cancelar",
                            on_click=State.cerrar_dialogo_sede,
                            variant="outline",
                            border_color=theme.Color.GRAY_500,
                            color=theme.Color.GRAY_900,
                            font_family=theme.Typography.FONT_FAMILY,
                            _hover={
                                "bg": theme.Color.GRAY_300,
                                "border_color": theme.Color.GRAY_700,
                            },
                        ),
                        rx.button(
                            rx.cond(
                                State.is_editing_sede,
                                "Guardar Cambios",
                                "Agregar Sede"
                            ),
                            on_click=State.guardar_sede,
                            bg="#004A99",
                            color=theme.Color.WHITE,
                            font_family=theme.Typography.FONT_FAMILY,
                            _hover={"bg": "#003875"},
                        ),
                        spacing="3",
                        justify="end",
                        width="100%",
                    ),
                    
                    spacing="6",
                    width="100%",
                ),
                bg=theme.Color.DARK_CARD,
                padding="24px",
                border_radius="12px",
                box_shadow="2xl",
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

def sede_action_buttons(sede: Dict[str, Any]) -> rx.Component:
    """Componente para los botones de acción de la fila de la sede."""
    return rx.hstack(
        rx.button(
            "Editar", 
            on_click=lambda: State.abrir_dialogo_editar_sede(sede),
            **ButtonStyle.secondary(),
            font_family=theme.Typography.FONT_FAMILY,
        ),
        rx.button(
            "Eliminar", 
            on_click=lambda: State.abrir_alerta_eliminar_sede(sede["id"]),
            **ButtonStyle.danger(),
            font_family=theme.Typography.FONT_FAMILY,
        ),
        spacing="2",
    )

def render_sede_row(sede: Dict[str, Any]) -> rx.Component:
    """Renderiza una fila de sede para la tabla."""
    return rx.table.row(
        rx.table.cell(sede["nombre"]),
        rx.table.cell(sede["direccion"]),
        rx.table.cell(sede["ciudad"]),
        rx.table.cell(sede["telefono"]),
        rx.table.cell(sede["email"]),
        rx.table.cell(sede["web"]),
        rx.table.cell(sede_action_buttons(sede)),
    )

def render_sede_card_mobile(sede: Dict[str, Any]) -> rx.Component:
    """Renderiza una tarjeta de sede para móvil."""
    return rx.box(
        rx.vstack(
            # Información principal
            rx.vstack(
                rx.heading(
                    sede["nombre"],
                    size="5",
                    font_family=theme.Typography.FONT_FAMILY,
                    font_weight=theme.Typography.FONT_WEIGHTS["semibold"],
                    color=theme.Color.GRAY_900,
                ),
                rx.text(
                    f"Dirección: {sede['direccion']}",
                    font_size="3",
                    color=theme.Color.GRAY_700,
                    font_family=theme.Typography.FONT_FAMILY,
                ),
                rx.text(
                    f"Ciudad: {sede['ciudad']}",
                    font_size="3",
                    color=theme.Color.GRAY_700,
                    font_family=theme.Typography.FONT_FAMILY,
                ),
                rx.text(
                    f"Teléfono: {sede['telefono']}",
                    font_size="3",
                    color=theme.Color.GRAY_700,
                    font_family=theme.Typography.FONT_FAMILY,
                ),
                rx.text(
                    f"Email: {sede['email']}",
                    font_size="3",
                    color=theme.Color.GRAY_700,
                    font_family=theme.Typography.FONT_FAMILY,
                ),
                rx.text(
                    f"Web: {sede['web']}",
                    font_size="3",
                    color=theme.Color.GRAY_700,
                    font_family=theme.Typography.FONT_FAMILY,
                ),
                spacing="2",
                align_items="start",
                width="100%",
            ),
            
            # Botones de acción
            rx.hstack(
                rx.button(
                    "Editar", 
                    on_click=lambda: State.abrir_dialogo_editar_sede(sede),
                    **ButtonStyle.secondary(),
                    font_family=theme.Typography.FONT_FAMILY,
                    flex="1",
                ),
                rx.button(
                    "Eliminar", 
                    on_click=lambda: State.abrir_alerta_eliminar_sede(sede["id"]),
                    **ButtonStyle.danger(),
                    font_family=theme.Typography.FONT_FAMILY,
                    flex="1",
                ),
                spacing="3",
                width="100%",
                margin_top="12px",
            ),
            
            spacing="4",
            align_items="start",
            width="100%",
        ),
        bg=theme.Color.DARK_CARD,
        border=f"1px solid {theme.Color.GRAY_500}",
        border_radius="12px",
        padding="16px",
        margin_bottom="12px",
        width="100%",
        _hover={
            "transform": "translateY(-2px)",
            "box_shadow": "0 4px 12px rgba(0,0,0,0.1)",
        },
        transition="all 0.2s ease-in-out",
    )

def admin_sedes_layout_desktop(*content) -> rx.Component:
    """Layout desktop para la página de administración de sedes."""
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
        # Navegación entre secciones
        rx.hstack(
            rx.button(
                "Gestión de Cursos",
                on_click=lambda: rx.redirect("/admin"),
                variant="outline",
                border_color=theme.Color.GRAY_500,
                color=theme.Color.GRAY_900,
                font_family=theme.Typography.FONT_FAMILY,
                _hover={
                    "bg": theme.Color.GRAY_300,
                    "border_color": theme.Color.GRAY_700,
                },
                border_radius="6px",
                padding="0.5em 1em",
            ),
            rx.button(
                "Gestión de Sedes",
                on_click=lambda: rx.redirect("/admin/sedes"),
                bg="#004A99",
                color=theme.Color.WHITE,
                font_family=theme.Typography.FONT_FAMILY,
                _hover={"bg": "#003875"},
                border_radius="6px",
                padding="0.5em 1em",
            ),
            rx.button(
                "Información de Institución",
                on_click=lambda: rx.redirect("/admin/instituciones"),
                variant="outline",
                border_color=theme.Color.GRAY_500,
                color=theme.Color.GRAY_900,
                font_family=theme.Typography.FONT_FAMILY,
                _hover={
                    "bg": theme.Color.GRAY_300,
                    "border_color": theme.Color.GRAY_700,
                },
                border_radius="6px",
                padding="0.5em 1em",
            ),
            spacing="2",
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

def admin_sedes_layout_mobile(*content) -> rx.Component:
    """Layout móvil para la página de administración de sedes."""
    return rx.vstack(
        rx.vstack(
            rx.heading(
                "Panel de Administración",
                color=theme.Color.GRAY_900,
                font_family=theme.Typography.FONT_FAMILY,
                size="6",
                text_align="center",
            ),
            rx.button(
                "Cerrar Sesión", 
                on_click=State.logout,
                **ButtonStyle.primary(),
                font_family=theme.Typography.FONT_FAMILY,
                width="100%",
            ),
            width="100%",
            padding="1em 1em",
            bg=theme.Color.GRAY_300,
            align_items="center",
            spacing="3",
        ),
        # Navegación entre secciones (móvil)
        rx.vstack(
            rx.button(
                "Gestión de Cursos",
                on_click=lambda: rx.redirect("/admin"),
                variant="outline",
                border_color=theme.Color.GRAY_500,
                color=theme.Color.GRAY_900,
                font_family=theme.Typography.FONT_FAMILY,
                _hover={
                    "bg": theme.Color.GRAY_300,
                    "border_color": theme.Color.GRAY_700,
                },
                border_radius="6px",
                padding="0.5em 1em",
                width="100%",
            ),
            rx.button(
                "Gestión de Sedes",
                on_click=lambda: rx.redirect("/admin/sedes"),
                bg="#004A99",
                color=theme.Color.WHITE,
                font_family=theme.Typography.FONT_FAMILY,
                _hover={"bg": "#003875"},
                border_radius="6px",
                padding="0.5em 1em",
                width="100%",
            ),
            rx.button(
                "Información de Institución",
                on_click=lambda: rx.redirect("/admin/instituciones"),
                variant="outline",
                border_color=theme.Color.GRAY_500,
                color=theme.Color.GRAY_900,
                font_family=theme.Typography.FONT_FAMILY,
                _hover={
                    "bg": theme.Color.GRAY_300,
                    "border_color": theme.Color.GRAY_700,
                },
                border_radius="6px",
                padding="0.5em 1em",
                width="100%",
            ),
            spacing="2",
            width="100%",
            padding="1em 1em",
            bg=theme.Color.GRAY_300,
            align_items="center"
        ),
        rx.box(
            *content,
            padding="1em",
            width="100%",
            flex_grow="1",
        ),
        min_height="100vh",
        width="100%",
        align_items="stretch",
        bg=theme.Color.GRAY_100,
    )

def admin_sedes_content_desktop() -> rx.Component:
    """Contenido de admin sedes para desktop."""
    return admin_sedes_layout_desktop(
        create_custom_dropdown_css(),
        rx.vstack(
            rx.hstack(
                rx.vstack(
                    rx.heading(
                        "Gestión de Sedes", 
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
                    "Agregar Nueva Sede", 
                    on_click=State.abrir_dialogo_agregar_sede,
                    **ButtonStyle.primary(),
                    font_family=theme.Typography.FONT_FAMILY,
                ),
                align_items="end",
                width="100%",
                margin_bottom="2em",
            ),
            
            rx.cond(
                State.admin_sedes,
                # Tabla tradicional para administración de sedes
                rx.table.root(
                    rx.table.header(
                        rx.table.row(
                            rx.table.cell("Nombre"),
                            rx.table.cell("Dirección"),
                            rx.table.cell("Ciudad"),
                            rx.table.cell("Teléfono"),
                            rx.table.cell("Email"),
                            rx.table.cell("Sitio Web"),
                            rx.table.cell("Acciones"),
                        )
                    ),
                    rx.table.body(
                        rx.foreach(State.admin_sedes, render_sede_row)
                    ),
                    width="100%",
                    bg=theme.Color.DARK_CARD,
                    border=f"1px solid {theme.Color.GRAY_500}",
                    border_radius="8px",
                ),
                # Mostrar mensaje cuando no hay sedes
                rx.box(
                    rx.text(
                        "No hay sedes registradas para esta institución.",
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

            sede_form_dialog(),
            spacing="0",
            width="100%",
            align_items="stretch",
        )
    )

def admin_sedes_content_mobile() -> rx.Component:
    """Contenido de admin sedes para móvil."""
    return admin_sedes_layout_mobile(
        create_custom_dropdown_css(),
        rx.vstack(
            # Header móvil
            rx.vstack(
                rx.heading(
                    "Gestión de Sedes", 
                    size="7",
                    color=theme.Color.BLUE_300,
                    font_family=theme.Typography.FONT_FAMILY,
                    font_weight=theme.Typography.FONT_WEIGHTS["bold"],
                    text_align="center",
                ),
                rx.cond(
                    State.logged_in_user,
                    rx.text(
                        f"Institución: {State.logged_in_user.institucion_nombre}",
                        color=theme.Color.GRAY_900,
                        font_family=theme.Typography.FONT_FAMILY,
                        text_align="center",
                        font_size="3",
                    ),
                    rx.text(
                        "Cargando...",
                        color=theme.Color.GRAY_700,
                        font_family=theme.Typography.FONT_FAMILY,
                        text_align="center",
                        font_size="3",
                    )
                ),
                rx.button(
                    "Agregar Nueva Sede", 
                    on_click=State.abrir_dialogo_agregar_sede,
                    **ButtonStyle.primary(),
                    font_family=theme.Typography.FONT_FAMILY,
                    width="100%",
                ),
                width="100%",
                spacing="4",
                margin_bottom="1.5em",
                align_items="center",
            ),
            
            # Contenido de sedes
            rx.cond(
                State.admin_sedes,
                # Vista de tarjetas para móvil
                rx.vstack(
                    rx.foreach(State.admin_sedes, render_sede_card_mobile),
                    spacing="0",
                    width="100%",
                ),
                # Mostrar mensaje cuando no hay sedes
                rx.box(
                    rx.text(
                        "No hay sedes registradas para esta institución.",
                        color=theme.Color.GRAY_700,
                        font_family=theme.Typography.FONT_FAMILY,
                        text_align="center",
                        font_size="3",
                    ),
                    padding="2em",
                    bg=theme.Color.DARK_CARD,
                    border=f"1px solid {theme.Color.GRAY_500}",
                        border_radius="8px",
                    width="100%",
                )
            ),

            sede_form_dialog(),
            spacing="0",
            width="100%",
            align_items="stretch",
        )
    )

@rx.page(route="/admin/sedes", on_load=[State.cargar_sedes_admin])
def admin_sedes_page() -> rx.Component:
    """Página de administración de sedes para usuarios logueados."""
    return rx.cond(
        State.logged_in_user,
        # Usuario autenticado - mostrar contenido admin responsive
        rx.box(
            rx.desktop_only(admin_sedes_content_desktop()),
            rx.mobile_and_tablet(admin_sedes_content_mobile()),
            width="100%",
            min_height="100vh",
            bg=theme.Color.GRAY_100,
        ),
        # Usuario no autenticado - redirigir al login
        rx.vstack(
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
    ) 