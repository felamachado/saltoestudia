# saltoestudia/pages/instituciones.py

import reflex as rx
from ..layout import page_layout, navbar_icons, footer, login_dialog
from ..state import State
from .. import theme

def render_institucion_card(institucion: dict) -> rx.Component:
    """Renderiza la tarjeta de una institución."""
    try:
        logo = institucion["logo"]
    except Exception:
        logo = "/logos/logoutu.png"
    try:
        nombre = institucion["nombre"]
    except Exception:
        nombre = ""
    try:
        direccion = institucion["direccion"]
    except Exception:
        direccion = ""
    try:
        telefono = institucion["telefono"]
    except Exception:
        telefono = ""
    try:
        email = institucion["email"]
    except Exception:
        email = ""
    try:
        web = institucion["web"]
    except Exception:
        web = ""
    return rx.box(
        rx.vstack(
            # Contenedor para logo con altura uniforme
            rx.box(
                rx.image(
                    src=logo, 
                    width="100%", 
                    height="120px",  # Altura fija uniforme para todos los logos
                    object_fit="contain",
                    padding="1em",
                    border_radius="8px",
                ),
                display="flex",
                justify_content="center",
                align_items="center",
                width="100%",
                height="140px",  # Altura fija del contenedor para alineación visual
                bg=theme.Color.WHITE,  # Fondo blanco para los logos
                border_radius="8px",
                margin_bottom="1em",
            ),
            
            # Contenido de texto con padding amplio
            rx.vstack(
                rx.heading(
                    nombre, 
                    size="5",  # Tamaño ligeramente mayor
                    font_weight=theme.Typography.FONT_WEIGHTS["bold"],
                    font_family=theme.Typography.FONT_FAMILY,
                    width="100%", 
                    text_align="center",
                    white_space="normal",
                    color=theme.Color.GRAY_900,
                    margin_bottom="1em",
                ),
                rx.divider(
                    border_color=theme.Color.GRAY_500,
                    margin_y="0.75em"
                ),
                rx.vstack(
                    rx.cond(
                        direccion,
                        rx.hstack(
                            rx.icon(tag="map_pin", size=18, color=theme.Color.BLUE_300), 
                            rx.text(
                                direccion,
                                font_size="0.9rem",
                                font_family=theme.Typography.FONT_FAMILY,
                                white_space="normal",
                                color=theme.Color.GRAY_700,
                                line_height="1.4",
                            ), 
                            spacing="3",
                            align_items="start",
                            width="100%",
                        )
                    ),
                    rx.cond(
                        telefono,
                        rx.hstack(
                            rx.icon(tag="phone", size=18, color=theme.Color.BLUE_300), 
                            rx.text(
                                telefono,
                                font_size="0.9rem",
                                font_family=theme.Typography.FONT_FAMILY,
                                white_space="normal",
                                color=theme.Color.GRAY_700,
                                line_height="1.4",
                            ), 
                            spacing="3",
                            align_items="center",
                            width="100%",
                        )
                    ),
                    rx.cond(
                        email,
                        rx.hstack(
                            rx.icon(tag="mail", size=18, color=theme.Color.BLUE_300), 
                            rx.text(
                                email,
                                font_size="0.9rem",
                                font_family=theme.Typography.FONT_FAMILY,
                                white_space="normal",
                                color=theme.Color.GRAY_700,
                                line_height="1.4",
                            ), 
                            spacing="3",
                            align_items="center",
                            width="100%",
                        )
                    ),
                    rx.cond(
                        web,
                        rx.hstack(
                            rx.icon(tag="globe", size=18, color=theme.Color.BLUE_300), 
                            rx.text(
                                "Sitio Web", 
                                font_size="0.9rem",
                                font_family=theme.Typography.FONT_FAMILY,
                                color=theme.Color.BLUE_300,
                                font_weight=theme.Typography.FONT_WEIGHTS["medium"],
                            ), 
                            spacing="3",
                            align_items="center",
                            width="100%",
                        )
                    ),
                    spacing="3", 
                    align_items="start", 
                    width="100%",
                ),
                width="100%", 
                spacing="2",
            ),
            spacing="0",
            width="100%",
            align_items="start",  # Alineación superior dentro de cada tarjeta
        ),
        # Padding interno amplio para que el contenido respire
        padding="2em",
        cursor="pointer",
        on_click=lambda: State.open_institution_dialog(institucion),
        bg=theme.Color.DARK_CARD,
        border=f"1px solid {theme.Color.GRAY_500}",
        border_radius="12px",
        box_shadow="lg",
        # Dimensiones para grilla automática optimizada
        width="100%",
        height="auto",
        # Transiciones suaves preservadas
        transition="all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
        _hover={
            "box_shadow": "2xl",
            "transform": "translateY(-4px)",
            "border_color": theme.Color.BLUE_300,
            "bg": theme.Color.GRAY_300,
        },
    )

def institution_dialog() -> rx.Component:
    """Diálogo que muestra información detallada de una institución."""
    return rx.cond(
        State.is_dialog_open,
        rx.box(
            rx.box(
                rx.vstack(
                    # Header del diálogo con logo y nombre
                    rx.hstack(
                        rx.image(
                            src=State.selected_institution["logo"],
                            width="60px",
                            height="60px",
                            object_fit="contain",
                            border_radius="8px",
                            background="lightgray",
                            padding="4px",
                        ),
                        rx.vstack(
                            rx.heading(
                                State.selected_institution["nombre"],
                                size="7",
                                font_family=theme.Typography.FONT_FAMILY,
                                font_weight=theme.Typography.FONT_WEIGHTS["bold"],
                                color=theme.Color.GRAY_900,  # on_surface
                            ),
                            rx.text(
                                "Información de la institución",
                                font_size="2",
                                color=theme.Color.GRAY_700,  # texto secundario
                                font_family=theme.Typography.FONT_FAMILY,
                            ),
                            align_items="start",
                            spacing="1",
                        ),
                        align_items="center",
                        spacing="4",
                        width="100%",
                    ),
                    
                    rx.divider(border_color=theme.Color.GRAY_500),  # border
                    
                    # Información detallada
                    rx.vstack(
                        rx.cond(
                            State.selected_institution["direccion"],
                            rx.hstack(
                                rx.icon(tag="info", size=18, color=theme.Color.BLUE_300),  # accent
                                rx.text(
                                    State.selected_institution["direccion"],
                                    font_family=theme.Typography.FONT_FAMILY,
                                    color=theme.Color.GRAY_900,  # on_surface
                                ),
                                align_items="start",
                                spacing="3",
                                width="100%",
                            )
                        ),
                        rx.cond(
                            State.selected_institution["telefono"],
                            rx.hstack(
                                rx.icon(tag="phone", size=18, color=theme.Color.BLUE_300),  # accent
                                rx.text(
                                    State.selected_institution["telefono"],
                                    font_family=theme.Typography.FONT_FAMILY,
                                    color=theme.Color.GRAY_900,  # on_surface
                                ),
                                align_items="center",
                                spacing="3",
                                width="100%",
                            )
                        ),
                        rx.cond(
                            State.selected_institution["email"],
                            rx.hstack(
                                rx.icon(tag="mail", size=18, color=theme.Color.BLUE_300),  # accent
                                rx.text(
                                    State.selected_institution["email"],
                                    font_family=theme.Typography.FONT_FAMILY,
                                    color=theme.Color.GRAY_900,  # on_surface
                                ),
                                align_items="center",
                                spacing="3",
                                width="100%",
                            )
                        ),
                        rx.cond(
                            State.selected_institution["web"],
                            rx.hstack(
                                rx.icon(tag="link", size=18, color=theme.Color.BLUE_300),  # accent
                                rx.text(
                                    "Sitio web disponible",
                                    color=theme.Color.BLUE_300,  # accent para enlaces
                                    font_family=theme.Typography.FONT_FAMILY,
                                    font_style="italic",
                                ),
                                align_items="center",
                                spacing="3",
                                width="100%",
                            )
                        ),
                        spacing="4",
                        align_items="start",
                        width="100%",
                    ),
                    
                    rx.divider(border_color=theme.Color.GRAY_500),  # border
                    
                    # Botones de acción
                    rx.hstack(
                        rx.button(
                            "Cerrar",
                            on_click=State.set_dialog_open(False),
                            variant="outline",
                            border_color=theme.Color.GRAY_500,  # border
                            color=theme.Color.GRAY_900,  # on_surface
                            font_family=theme.Typography.FONT_FAMILY,
                            _hover={
                                "bg": theme.Color.GRAY_300,  # hover más claro
                                "border_color": theme.Color.GRAY_700,
                            },
                        ),
                        rx.button(
                            "Ver Cursos",
                            on_click=State.go_to_institution_courses,
                            bg="#004A99",  # primary
                            color=theme.Color.WHITE,  # on_primary
                            font_family=theme.Typography.FONT_FAMILY,
                            _hover={"bg": "#003875"},  # primary más oscuro
                        ),
                        spacing="3",
                        justify="end",
                        width="100%",
                    ),
                    
                    spacing="6",
                    width="100%",
                ),
                bg=theme.Color.DARK_CARD,  # surface
                padding="24px",
                border_radius="12px",
                box_shadow="2xl",  # conservo la misma elevación
                max_width="500px",
                width="90%",
                border=f"1px solid {theme.Color.GRAY_500}",  # border sutil
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

@rx.page(
    route="/instituciones",
    title="Instituciones | Salto Estudia",
    on_load=State.cargar_instituciones
)
def instituciones() -> rx.Component:
    # Layout especializado para instituciones sin limitaciones de ancho
    from ..layout import navbar_icons, footer, login_dialog, mobile_menu
    
    return rx.box(
        rx.vstack(
            navbar_icons(),
            mobile_menu(),  # Agregar el menú móvil
            # Contenedor principal sin limitaciones de max-width
            rx.box(
                # Contenedor centrado que no desborda
                rx.box(
                    rx.vstack(
                        # Título principal
                        rx.heading(
                            "Instituciones Educativas", 
                            size="9", 
                            color=theme.Color.BLUE_300,
                            font_family=theme.Typography.FONT_FAMILY,
                            font_weight=theme.Typography.FONT_WEIGHTS["bold"],
                            margin_bottom="0.5em"
                        ),
                        # Subtítulo
                        rx.text(
                            "Aquí encontrarás las principales instituciones educativas de Salto.",
                            size="4",
                            color=theme.Color.GRAY_900,
                            font_family=theme.Typography.FONT_FAMILY,
                            text_align="center",
                            margin_bottom="2em",
                        ),
                        
                        rx.cond(
                            State.instituciones_info,
                            # Grilla optimizada centrada sin desbordamiento
                            rx.box(
                                rx.foreach(State.instituciones_info, render_institucion_card),
                                # CSS Grid con distribución automática controlada
                                display="grid",
                                grid_template_columns="repeat(auto-fill, minmax(260px, 1fr))",
                                grid_auto_rows="auto",
                                gap="2em",
                                width="100%",
                                align_items="start",
                                justify_items="stretch",
                            ),
                            rx.text(
                                "No se pudieron cargar las instituciones en este momento.", 
                                color=theme.Color.GRAY_700,
                                font_family=theme.Typography.FONT_FAMILY,
                            )
                        ),
                        
                        spacing="8",
                        width="100%",
                        align_items="center",
                    ),
                    
                    # Contenedor principal con dimensiones controladas
                    width="95%",  # 95% del viewport
                    max_width="1440px",  # Máximo 1440px como solicitaste
                    margin_x="auto",  # Centrado horizontal
                    padding_x="1rem",  # Padding interno mínimo
                    padding_y="2em",
                    # Prevenir scroll horizontal
                    overflow_x="hidden",
                    box_sizing="border-box",
                ),
                
                # Contenedor wrapper que ocupa todo el ancho disponible
                width="100%",
                flex_grow="1",
                bg=theme.Color.GRAY_100,
                # Asegurar que no hay overflow horizontal
                overflow_x="hidden",
            ),
            footer(),
            
            # Layout principal sin overflow horizontal
            min_height="100vh",
            width="100%",
            align_items="center",
            spacing="0",
            bg=theme.Color.GRAY_100,
        ),
        
        # Componentes overlay
        login_dialog(),
        institution_dialog(),
        
        # Contenedor raíz sin overflow horizontal
        overflow_x="hidden",
        width="100%",
        position="relative",
    )
