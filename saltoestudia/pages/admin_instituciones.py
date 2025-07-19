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
        
        # Formulario para editar institución
        rx.box(
            rx.vstack(
                rx.heading(
                    "Editar Información de la Institución",
                    size="5",
                    font_family=theme.Typography.FONT_FAMILY,
                    font_weight=theme.Typography.FONT_WEIGHTS["semibold"],
                    color=theme.Color.GRAY_900,
                    margin_bottom="2em",
                ),
                
                # Formulario usando rx.form para el nombre
                rx.form.root(
                    rx.vstack(
                        # Campo Nombre
                        rx.form.field(
                            rx.vstack(
                                rx.form.label(
                                    "Nombre de la institución",
                                    **ComponentStyle.FORM_LABEL
                                ),
                                rx.form.control(
                                    rx.input(
                                        name="institucion_nombre",
                                        placeholder="Ej: UDELAR – CENUR LN",
                                        value=State.form_institucion_nombre,
                                        required=True,
                                        **ComponentStyle.FORM_INPUT,
                                    ),
                                    as_child=True,
                                ),
                                rx.form.message(
                                    "El nombre de la institución es obligatorio",
                                    match="valueMissing",
                                    color="red.500",
                                    font_size="14px",
                                ),
                                align_items="start", 
                                width="100%"
                            ),
                            name="institucion_nombre",
                        ),
                        
                        spacing="4",
                        width="100%",
                    ),
                    on_submit=State.handle_institucion_form_submit,
                    reset_on_submit=False,
                ),
                
                # Separador
                rx.divider(margin_y="1em"),
                
                # Sección de carga de logo usando rx.upload
                rx.vstack(
                    rx.heading(
                        "Logo de la Institución",
                        size="6",
                        font_family=theme.Typography.FONT_FAMILY,
                        font_weight=theme.Typography.FONT_WEIGHTS["semibold"],
                        color=theme.Color.GRAY_900,
                        margin_bottom="0.5em",
                    ),
                    
                    # Componente de carga de archivos usando rx.upload
                    rx.upload(
                        rx.vstack(
                            rx.button(
                                "Seleccionar Imagen",
                                **ButtonStyle.primary(),
                                font_family=theme.Typography.FONT_FAMILY,
                                size="2",
                            ),
                            rx.text(
                                "Arrastra una imagen aquí o haz clic para seleccionar",
                                color="#6b7280",
                                font_size="12px",
                                text_align="center",
                            ),
                            align_items="center",
                            spacing="1",
                            padding="0.5em",
                            width="100%",
                        ),
                        accept={
                            "image/*": [".png", ".jpg", ".jpeg", ".gif", ".webp"]
                        },
                        max_files=1,
                        on_drop=State.handle_file_upload,
                        border="2px dashed #d1d5db",
                        border_radius="6px",
                        bg="gray.50",
                        _hover={"bg": "gray.100"},
                        padding="1em",
                        width="100%",
                    ),
                    
                    # Vista previa del logo actual
                    rx.cond(
                        State.form_institucion_logo,
                        rx.vstack(
                            rx.text("Logo actual", font_size="14px", color="#6b7280", font_weight="medium"),
                            rx.image(
                                src=State.form_institucion_logo,
                                width="150px",
                                height="100px",
                                object_fit="contain",
                                border="2px solid #e5e7eb",
                                border_radius="8px",
                                padding="1em",
                                bg="white",
                                box_shadow="sm",
                            ),
                            rx.button(
                                "Eliminar Logo",
                                on_click=State.limpiar_logo,
                                variant="outline",
                                color="red.500",
                                border_color="red.500",
                                font_family=theme.Typography.FONT_FAMILY,
                                size="2",
                                _hover={"bg": "red.50"},
                                margin_top="0.5em",
                            ),
                            align_items="center",
                            spacing="2",
                        ),
                        rx.text(
                            "No hay logo configurado",
                            color="#6b7280",
                            font_size="12px",
                            text_align="center",
                        ),
                    ),
                    
                    align_items="start", 
                    width="100%",
                    spacing="2",
                ),
                
                # Separador antes del botón de guardado
                rx.divider(margin_y="1em"),
                
                # Botón de guardado al final
                rx.button(
                    "Guardar Cambios",
                    **ButtonStyle.primary(),
                    font_family=theme.Typography.FONT_FAMILY,
                    width="100%",
                    size="3",
                    padding="1em",
                ),
                
                spacing="3",
                width="100%",
            ),
            padding="1.5em",
            bg=theme.Color.DARK_CARD,
            border=f"1px solid {theme.Color.GRAY_500}",
            border_radius="12px",
            box_shadow="lg",
            width="100%",
            max_width="600px",
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
        
        # Formulario para editar institución (móvil)
        rx.box(
            rx.vstack(
                rx.heading(
                    "Editar Información de la Institución",
                    size="6",
                    font_family=theme.Typography.FONT_FAMILY,
                    font_weight=theme.Typography.FONT_WEIGHTS["semibold"],
                    color=theme.Color.GRAY_900,
                    margin_bottom="1.5em",
                ),
                
                # Formulario usando rx.form para el nombre
                rx.form.root(
                    rx.vstack(
                        # Campo Nombre
                        rx.form.field(
                            rx.vstack(
                                rx.form.label(
                                    "Nombre de la institución",
                                    **ComponentStyle.FORM_LABEL
                                ),
                                rx.form.control(
                                    rx.input(
                                        name="institucion_nombre",
                                        placeholder="Ej: UDELAR – CENUR LN",
                                        value=State.form_institucion_nombre,
                                        required=True,
                                        **ComponentStyle.FORM_INPUT,
                                    ),
                                    as_child=True,
                                ),
                                rx.form.message(
                                    "El nombre de la institución es obligatorio",
                                    match="valueMissing",
                                    color="red.500",
                                    font_size="14px",
                                ),
                                align_items="start", 
                                width="100%"
                            ),
                            name="institucion_nombre",
                        ),
                        
                        spacing="3",
                        width="100%",
                    ),
                    on_submit=State.handle_institucion_form_submit,
                    reset_on_submit=False,
                ),
                
                # Separador
                rx.divider(margin_y="1em"),
                
                # Sección de carga de logo usando rx.upload (móvil)
                rx.vstack(
                    rx.heading(
                        "Logo de la Institución",
                        size="6",
                        font_family=theme.Typography.FONT_FAMILY,
                        font_weight=theme.Typography.FONT_WEIGHTS["semibold"],
                        color=theme.Color.GRAY_900,
                        margin_bottom="0.5em",
                    ),
                    
                    # Componente de carga de archivos usando rx.upload (móvil)
                    rx.upload(
                        rx.vstack(
                            rx.button(
                                "Seleccionar Imagen",
                                **ButtonStyle.primary(),
                                font_family=theme.Typography.FONT_FAMILY,
                                size="2",
                                width="100%",
                            ),
                            rx.text(
                                "Arrastra una imagen aquí o haz clic para seleccionar",
                                color="#6b7280",
                                font_size="12px",
                                text_align="center",
                            ),
                            align_items="center",
                            spacing="1",
                            padding="0.5em",
                            width="100%",
                        ),
                        accept={
                            "image/*": [".png", ".jpg", ".jpeg", ".gif", ".webp"]
                        },
                        max_files=1,
                        on_drop=State.handle_file_upload,
                        border="2px dashed #d1d5db",
                        border_radius="6px",
                        bg="gray.50",
                        _hover={"bg": "gray.100"},
                        padding="1em",
                        width="100%",
                    ),
                    
                    # Vista previa del logo actual
                    rx.cond(
                        State.form_institucion_logo,
                        rx.vstack(
                            rx.text("Logo actual", font_size="14px", color="#6b7280", font_weight="medium"),
                            rx.image(
                                src=State.form_institucion_logo,
                                width="120px",
                                height="80px",
                                object_fit="contain",
                                border="2px solid #e5e7eb",
                                border_radius="8px",
                                padding="0.8em",
                                bg="white",
                                box_shadow="sm",
                            ),
                            rx.button(
                                "Eliminar Logo",
                                on_click=State.limpiar_logo,
                                variant="outline",
                                color="red.500",
                                border_color="red.500",
                                font_family=theme.Typography.FONT_FAMILY,
                                size="2",
                                _hover={"bg": "red.50"},
                                margin_top="0.5em",
                            ),
                            align_items="center",
                            spacing="2",
                        ),
                        rx.text(
                            "No hay logo configurado",
                            color="#6b7280",
                            font_size="12px",
                            text_align="center",
                        ),
                    ),
                    
                    align_items="center", 
                    width="100%",
                    spacing="2",
                ),
                
                # Separador antes del botón de guardado
                rx.divider(margin_y="1em"),
                
                # Botón de guardado al final
                rx.button(
                    "Guardar Cambios",
                    **ButtonStyle.primary(),
                    font_family=theme.Typography.FONT_FAMILY,
                    width="100%",
                    size="3",
                    padding="1em",
                ),
                
                spacing="2",
                width="100%",
            ),
            padding="1em",
            bg=theme.Color.DARK_CARD,
            border=f"1px solid {theme.Color.GRAY_500}",
            border_radius="12px",
            box_shadow="lg",
            width="100%",
        ),
        
        spacing="2",
        width="100%",
        align_items="center",
    )

@rx.page(
    route="/admin/instituciones",
    on_load=[State.cargar_institucion_actual]
)
def admin_instituciones_page() -> rx.Component:
    """Página de administración de información de institución."""
    
    # Verificar autenticación
    if not State.is_authenticated():
        return State.require_admin_access()
    
    # Layout responsive
    return rx.cond(
        State.is_mobile,
        admin_instituciones_layout_mobile(
            admin_instituciones_content_mobile()
        ),
        admin_instituciones_layout_desktop(
            admin_instituciones_content_desktop()
        )
    ) 