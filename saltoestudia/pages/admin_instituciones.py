# saltoestudia/pages/admin_instituciones.py

import reflex as rx
from ..state import State
from .. import theme
from ..theme import ButtonStyle, ComponentStyle
from typing import Dict, Any

def admin_instituciones_layout_desktop(*content) -> rx.Component:
    """Layout desktop para la página de administración de instituciones."""
    return rx.vstack(
        rx.hstack(
            rx.heading(
                "Administración de Institución",
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
                "Información de Institución",
                on_click=lambda: rx.redirect("/admin/instituciones"),
                bg="#004A99",
                color=theme.Color.WHITE,
                font_family=theme.Typography.FONT_FAMILY,
                _hover={"bg": "#003875"},
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

def admin_instituciones_layout_mobile(*content) -> rx.Component:
    """Layout móvil para la página de administración de instituciones."""
    return rx.vstack(
        rx.vstack(
            rx.heading(
                "Administración de Institución",
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
                "Información de Institución",
                on_click=lambda: rx.redirect("/admin/instituciones"),
                bg="#004A99",
                color=theme.Color.WHITE,
                font_family=theme.Typography.FONT_FAMILY,
                _hover={"bg": "#003875"},
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

def institucion_form_dialog() -> rx.Component:
    """Diálogo que contiene el formulario para editar la información de la institución."""
    return rx.cond(
        State.show_institucion_dialog,
        rx.box(
            rx.box(
                rx.vstack(
                    # Header del diálogo
                    rx.hstack(
                        rx.heading(
                            "Editar Información de Institución",
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
                            rx.text("Nombre de la institución", **ComponentStyle.FORM_LABEL),
                            rx.input(
                                value=State.form_institucion_nombre,
                                on_change=State.set_form_institucion_nombre,
                                placeholder="Ej: UDELAR – CENUR LN",
                                **ComponentStyle.FORM_INPUT,
                            ),
                            align_items="start", width="100%",
                        ),
                        
                        # Campo Logo
                        rx.vstack(
                            rx.text("Logo de la institución", **ComponentStyle.FORM_LABEL),
                            rx.text(
                                "Ruta al archivo de logo (ej: /logos/logo-cenur.png)",
                                color="#6b7280",
                                font_size="14px",
                                margin_bottom="8px",
                            ),
                            rx.input(
                                value=State.form_institucion_logo,
                                on_change=State.set_form_institucion_logo,
                                placeholder="/logos/logo-cenur.png",
                                **ComponentStyle.FORM_INPUT,
                            ),
                            # Vista previa del logo
                            rx.cond(
                                State.form_institucion_logo,
                                rx.box(
                                    rx.text("Vista previa:", **ComponentStyle.FORM_LABEL),
                                    rx.image(
                                        src=State.form_institucion_logo,
                                        width="200px",
                                        height="120px",
                                        object_fit="contain",
                                        border="1px solid #e5e7eb",
                                        border_radius="8px",
                                        padding="1em",
                                        bg="white",
                                    ),
                                    align_items="start", width="100%",
                                ),
                                rx.text(
                                    "No hay logo configurado",
                                    color="#9ca3af",
                                    font_size="14px",
                                    padding="1em",
                                    border="1px solid #e5e7eb",
                                    border_radius="6px",
                                    background_color="#f9fafb",
                                ),
                            ),
                            align_items="start", width="100%",
                        ),
                        
                        spacing="4",
                        padding_y="1em",
                        width="100%",
                    ),
                    
                    rx.divider(border_color=theme.Color.GRAY_500),
                    
                    # Botones de acción - Responsive
                    rx.box(
                        # Desktop: horizontal
                        rx.desktop_only(
                            rx.hstack(
                                rx.button(
                                    "Cancelar",
                                    on_click=State.cerrar_dialogo_institucion,
                                    **ButtonStyle.secondary(),
                                    font_family=theme.Typography.FONT_FAMILY,
                                ),
                                rx.button(
                                    "Guardar Cambios",
                                    on_click=State.guardar_institucion,
                                    **ButtonStyle.primary(),
                                    font_family=theme.Typography.FONT_FAMILY,
                                ),
                                spacing="3",
                                justify="end",
                                width="100%",
                            ),
                        ),
                        # Móvil: vertical, botones full width
                        rx.mobile_and_tablet(
                            rx.vstack(
                                rx.button(
                                    "Guardar Cambios",
                                    on_click=State.guardar_institucion,
                                    **ButtonStyle.primary(),
                                    font_family=theme.Typography.FONT_FAMILY,
                                    width="100%",
                                ),
                                rx.button(
                                    "Cancelar",
                                    on_click=State.cerrar_dialogo_institucion,
                                    **ButtonStyle.secondary(),
                                    font_family=theme.Typography.FONT_FAMILY,
                                    width="100%",
                                ),
                                spacing="3",
                                width="100%",
                            ),
                        ),
                        width="100%",
                    ),
                    
                    spacing="4",
                    width="100%",
                ),
                **ComponentStyle.MODAL,
                padding="16px",
                max_width="500px",
                width="95%",
                max_height="90vh",
                overflow_y="auto",
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

def admin_instituciones_content_desktop() -> rx.Component:
    """Contenido desktop para la administración de instituciones."""
    return rx.vstack(
        rx.heading(
            "Información de la Institución",
            size="4",
            font_family=theme.Typography.FONT_FAMILY,
            font_weight=theme.Typography.FONT_WEIGHTS["bold"],
            color=theme.Color.GRAY_900,
            margin_bottom="2em",
        ),
        
        # Tarjeta de información actual
        rx.box(
            rx.vstack(
                rx.heading(
                    "Datos Actuales",
                    size="5",
                    font_family=theme.Typography.FONT_FAMILY,
                    font_weight=theme.Typography.FONT_WEIGHTS["semibold"],
                    color=theme.Color.GRAY_900,
                    margin_bottom="1em",
                ),
                
                rx.hstack(
                    # Logo actual
                    rx.box(
                        rx.image(
                            src=State.institucion_actual.get("logo", "/logos/logoutu.png"),
                            width="200px",
                            height="120px",
                            object_fit="contain",
                            border="1px solid #e5e7eb",
                            border_radius="8px",
                            padding="1em",
                            bg="white",
                        ),
                        margin_right="2em",
                    ),
                    
                    # Información de la institución
                    rx.vstack(
                        rx.text(
                            f"Nombre: {State.institucion_actual.get('nombre', 'No disponible')}",
                            font_size="1.1rem",
                            font_family=theme.Typography.FONT_FAMILY,
                            color=theme.Color.GRAY_700,
                            font_weight=theme.Typography.FONT_WEIGHTS["medium"],
                        ),
                        rx.text(
                            f"Logo: {State.institucion_actual.get('logo', '/logos/logoutu.png')}",
                            font_size="1rem",
                            font_family=theme.Typography.FONT_FAMILY,
                            color=theme.Color.GRAY_600,
                        ),
                        rx.text(
                            f"ID: {State.institucion_actual.get('id', 'N/A')}",
                            font_size="0.9rem",
                            font_family=theme.Typography.FONT_FAMILY,
                            color=theme.Color.GRAY_500,
                        ),
                        align_items="start",
                        spacing="1",
                    ),
                    
                    spacing="2",
                    align_items="start",
                    width="100%",
                ),
                
                # Botón de editar
                rx.button(
                    "Editar Información",
                    on_click=State.abrir_dialogo_editar_institucion,
                    **ButtonStyle.primary(),
                    font_family=theme.Typography.FONT_FAMILY,
                    margin_top="2em",
                ),
                
                spacing="3",
                width="100%",
            ),
            padding="2em",
            bg=theme.Color.WHITE,
            border=f"1px solid {theme.Color.GRAY_300}",
            border_radius="12px",
            box_shadow="lg",
            width="100%",
            max_width="800px",
        ),
        
        spacing="4",
        width="100%",
        align_items="center",
    )

def admin_instituciones_content_mobile() -> rx.Component:
    """Contenido móvil para la administración de instituciones."""
    return rx.vstack(
        rx.heading(
            "Información de la Institución",
            size="5",
            font_family=theme.Typography.FONT_FAMILY,
            font_weight=theme.Typography.FONT_WEIGHTS["bold"],
            color=theme.Color.GRAY_900,
            text_align="center",
            margin_bottom="1.5em",
        ),
        
        # Tarjeta de información actual
        rx.box(
            rx.vstack(
                rx.heading(
                    "Datos Actuales",
                    size="6",
                    font_family=theme.Typography.FONT_FAMILY,
                    font_weight=theme.Typography.FONT_WEIGHTS["semibold"],
                    color=theme.Color.GRAY_900,
                    margin_bottom="1em",
                    text_align="center",
                ),
                
                # Logo actual
                rx.box(
                    rx.image(
                        src=State.institucion_actual.get("logo", "/logos/logoutu.png"),
                        width="100%",
                        max_width="200px",
                        height="120px",
                        object_fit="contain",
                        border="1px solid #e5e7eb",
                        border_radius="8px",
                        padding="1em",
                        bg="white",
                    ),
                    display="flex",
                    justify_content="center",
                    margin_bottom="1em",
                ),
                
                # Información de la institución
                rx.vstack(
                    rx.text(
                        f"Nombre: {State.institucion_actual.get('nombre', 'No disponible')}",
                        font_size="1rem",
                        font_family=theme.Typography.FONT_FAMILY,
                        color=theme.Color.GRAY_700,
                        font_weight=theme.Typography.FONT_WEIGHTS["medium"],
                        text_align="center",
                    ),
                    rx.text(
                        f"Logo: {State.institucion_actual.get('logo', '/logos/logoutu.png')}",
                        font_size="0.9rem",
                        font_family=theme.Typography.FONT_FAMILY,
                        color=theme.Color.GRAY_600,
                        text_align="center",
                    ),
                    rx.text(
                        f"ID: {State.institucion_actual.get('id', 'N/A')}",
                        font_size="0.8rem",
                        font_family=theme.Typography.FONT_FAMILY,
                        color=theme.Color.GRAY_500,
                        text_align="center",
                    ),
                    align_items="center",
                    spacing="1",
                    width="100%",
                ),
                
                # Botón de editar
                rx.button(
                    "Editar Información",
                    on_click=State.abrir_dialogo_editar_institucion,
                    **ButtonStyle.primary(),
                    font_family=theme.Typography.FONT_FAMILY,
                    margin_top="1.5em",
                    width="100%",
                ),
                
                spacing="3",
                width="100%",
            ),
            padding="1.5em",
            bg=theme.Color.WHITE,
            border=f"1px solid {theme.Color.GRAY_300}",
            border_radius="12px",
            box_shadow="lg",
            width="100%",
        ),
        
        spacing="4",
        width="100%",
        align_items="center",
    )

@rx.page(
    route="/admin/instituciones",
    on_load=[State.cargar_institucion_actual]
)
def admin_instituciones_page() -> rx.Component:
    """Página de administración de información de la institución."""
    return rx.cond(
        State.is_mobile,
        admin_instituciones_layout_mobile(
            admin_instituciones_content_mobile(),
            institucion_form_dialog(),
        ),
        admin_instituciones_layout_desktop(
            admin_instituciones_content_desktop(),
            institucion_form_dialog(),
        ),
    ) 