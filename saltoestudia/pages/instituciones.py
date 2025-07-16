# saltoestudia/pages/instituciones.py

import reflex as rx
from ..layout import page_layout, navbar_icons, footer, login_dialog
from ..state import State
from .. import theme
from ..theme import ComponentStyle



def render_institucion_card(sede) -> rx.Component:
    """Renderiza la tarjeta de una sede de institución."""
    logo = sede.get("logo", "/logos/logoutu.png")
    nombre = sede.get("nombre", "")
    ciudad = sede.get("ciudad", "")

    return rx.box(
        rx.vstack(
            rx.box(
                rx.image(
                    src=logo,
                    width="100%",
                    height="120px",
                    object_fit="contain",
                    padding="1em",
                    border_radius="8px",
                ),
                display="flex",
                justify_content="center",
                align_items="center",
                width="100%",
                height="140px",
                bg=theme.Color.WHITE,
                border_radius="8px",
                margin_bottom="1em",
            ),
            rx.vstack(
                rx.heading(
                    nombre,
                    size="5",
                    font_weight=theme.Typography.FONT_WEIGHTS["bold"],
                    font_family=theme.Typography.FONT_FAMILY,
                    width="100%",
                    text_align="center",
                    white_space="normal",
                    color=theme.Color.GRAY_900,
                    margin_bottom="0.5em",
                ),

                width="100%",
                spacing="2",
            ),
            spacing="0",
            width="100%",
            align_items="start",
        ),
        padding="2em",
        cursor="pointer",
        on_click=lambda: State.open_institution_dialog(sede),
        bg=theme.Color.DARK_CARD,
        border=f"1px solid {theme.Color.GRAY_500}",
        border_radius="12px",
        box_shadow="lg",
        width="100%",
        height="auto",
        transition="all 0.3s cubic-bezier(0.4, 0, 0.2, 1)",
        _hover={
            "box_shadow": "2xl",
            "transform": "translateY(-4px)",
            "border_color": theme.Color.BLUE_300,
            "bg": theme.Color.GRAY_300,
        },
    )

def render_sede_info(sede: dict) -> rx.Component:
    """Renderiza la información de una sede individual."""
    direccion = sede["direccion"]
    ciudad = sede["ciudad"]
    
    return rx.vstack(
        rx.vstack(
            rx.cond(
                ciudad == "Virtual",
                # Información para sede virtual
                rx.vstack(
                    rx.text(
                        "Modalidad: Virtual",
                        font_size="0.9rem",
                        font_family=theme.Typography.FONT_FAMILY,
                        color=theme.Color.GRAY_700,
                        font_weight=theme.Typography.FONT_WEIGHTS["medium"],
                    ),
                    rx.text(
                        "Tipo: Cursos online",
                        font_size="0.9rem",
                        font_family=theme.Typography.FONT_FAMILY,
                        color=theme.Color.GRAY_700,
                    ),
                    rx.text(
                        "Acceso: Desde cualquier lugar",
                        font_size="0.9rem",
                        font_family=theme.Typography.FONT_FAMILY,
                        color=theme.Color.GRAY_700,
                    ),
                    spacing="2",
                    align_items="start",
                    width="100%",
                ),
                # Información para sede física
                rx.vstack(
                    rx.text(
                        f"Ciudad: {ciudad}",
                        font_size="0.9rem",
                        font_family=theme.Typography.FONT_FAMILY,
                        color=theme.Color.GRAY_700,
                        font_weight=theme.Typography.FONT_WEIGHTS["medium"],
                    ),
                    rx.text(
                        f"Dirección: {direccion}",
                        font_size="0.9rem",
                        font_family=theme.Typography.FONT_FAMILY,
                        color=theme.Color.GRAY_700,
                    ),
                    rx.text(
                        f"Teléfono: {sede['telefono']}",
                        font_size="0.9rem",
                        font_family=theme.Typography.FONT_FAMILY,
                        color=theme.Color.GRAY_700,
                    ),
                    rx.text(
                        f"Email: {sede['email']}",
                        font_size="0.9rem",
                        font_family=theme.Typography.FONT_FAMILY,
                        color=theme.Color.GRAY_700,
                    ),
                    rx.cond(
                        sede.get("web"),
                        rx.hstack(
                            rx.text(
                                "Sitio web:",
                                font_size="0.9rem",
                                font_family=theme.Typography.FONT_FAMILY,
                                color=theme.Color.GRAY_700,
                            ),
                            rx.link(
                                sede["web"],
                                href=sede["web"],
                                is_external=True,
                                font_size="0.9rem",
                                font_family=theme.Typography.FONT_FAMILY,
                                color=theme.Color.BLUE_700,
                                _hover={"text_decoration": "underline"},
                            ),
                            spacing="1",
                            align_items="center",
                        ),
                        rx.text(
                            "Sitio web: No disponible",
                            font_size="0.9rem",
                            font_family=theme.Typography.FONT_FAMILY,
                            color=theme.Color.GRAY_700,
                        )
                    ),
                    spacing="2",
                    align_items="start",
                    width="100%",
                )
            ),
            spacing="2",
            align_items="start",
            width="100%",
        ),
        # Botón "Ver Cursos" específico para esta sede
        rx.button(
            rx.cond(
                ciudad == "Virtual",
                "Ver cursos virtuales",
                f"Ver Cursos en {ciudad}"
            ),
            on_click=lambda: State.go_to_sede_courses(sede),
            bg="#004A99",  # primary
            color=theme.Color.WHITE,  # on_primary
            font_family=theme.Typography.FONT_FAMILY,
            font_size="0.9rem",
            padding="0.5em 1em",
            border_radius="6px",
            _hover={"bg": "#003875"},  # primary más oscuro
            margin_top="1em",
            align_self="end",  # Alinear a la derecha
        ),
        spacing="3",
        align_items="start",
        width="100%",
        padding="1em",
        bg=theme.Color.GRAY_100,
        border_radius="8px",
        border=f"1px solid {theme.Color.GRAY_300}",
    )

def render_sede_acordeon_item(sede: dict) -> rx.Component:
    """Renderiza un elemento del acordeón para una sede."""
    
    return rx.vstack(
        # Header del acordeón (siempre visible)
        rx.box(
            rx.hstack(
                rx.heading(
                    sede["nombre"],
                    size="4",
                    font_family=theme.Typography.FONT_FAMILY,
                    font_weight=theme.Typography.FONT_WEIGHTS["medium"],
                    color=theme.Color.GRAY_900,
                ),
                rx.spacer(),
                rx.cond(
                    State.expanded_sede_id == sede["id"],
                    rx.icon(
                        tag="chevron_down",
                        size=20,
                        color=theme.Color.GRAY_700,
                        transition="transform 0.2s ease",
                        transform="rotate(90deg)",
                    ),
                    rx.icon(
                        tag="chevron_right",
                        size=20,
                        color=theme.Color.GRAY_700,
                        transition="transform 0.2s ease",
                        transform="rotate(0deg)",
                    ),
                ),
                width="100%",
                align_items="center",
                cursor="pointer",
                padding="1em",
                bg=theme.Color.DARK_CARD,
                border_radius="8px",
                border=f"1px solid {theme.Color.GRAY_500}",
                _hover={
                    "bg": theme.Color.GRAY_300,
                    "border_color": theme.Color.BLUE_300,
                },
                on_click=lambda: State.toggle_sede_acordeon(sede["id"]),
            ),
            width="100%",
        ),
        # Contenido del acordeón (condicional)
        rx.cond(
            State.expanded_sede_id == sede["id"],
            rx.box(
                render_sede_info(sede),
                width="100%",
                margin_top="0.5em",
            ),
        ),
        spacing="0",
        width="100%",
    )

def institution_dialog() -> rx.Component:
    """Diálogo que muestra información detallada de las sedes de una institución."""
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
                                rx.cond(
                                    State.selected_institution.get("ciudad") == "Virtual",
                                    "Cursos virtuales disponibles",
                                    rx.cond(
                                        State.selected_institution_sedes.length() == 1,
                                        "1 sede física",
                                        rx.cond(
                                            State.selected_institution_sedes.length() == 0,
                                            "Sin sedes físicas",
                                            f"{State.selected_institution_sedes.length()} sedes físicas"
                                        )
                                    )
                                ),
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

                    # Contenido de sedes
                    rx.cond(
                        State.selected_institution_sedes.length() == 1,
                        # Si solo hay una sede, mostrarla directamente
                        render_sede_info(State.selected_institution_sedes[0]),
                        # Si hay múltiples sedes, usar acordeón
                        rx.vstack(
                            rx.foreach(
                                State.selected_institution_sedes,
                                lambda sede: render_sede_acordeon_item(sede)
                            ),
                            spacing="2",
                            align_items="start",
                            width="100%",
                        )
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
                max_width="600px",  # Aumentado para acomodar el acordeón
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
    on_load=State.cargar_datos_instituciones_page
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
                            "Sedes de Instituciones Educativas", 
                            size="9", 
                            color=theme.Color.BLUE_300,
                            font_family=theme.Typography.FONT_FAMILY,
                            font_weight=theme.Typography.FONT_WEIGHTS["bold"],
                            margin_bottom="0.5em"
                        ),
                        # Subtítulo
                        rx.text(
                            "Aquí encontrarás todas las sedes físicas de las instituciones educativas.",
                            size="4",
                            color=theme.Color.GRAY_900,
                            font_family=theme.Typography.FONT_FAMILY,
                            text_align="center",
                            margin_bottom="1em",
                        ),
                        
                        # Filtro por ciudad
                        rx.vstack(
                            rx.text(
                                "Filtrar por ciudad:",
                                font_size="1rem",
                                font_family=theme.Typography.FONT_FAMILY,
                                color=theme.Color.GRAY_900,
                                font_weight=theme.Typography.FONT_WEIGHTS["medium"],
                            ),
                            rx.select(
                                State.ciudades_nombres,
                                placeholder="Selecciona ciudad",
                                value=State.ciudad_filtro_instituciones,
                                on_change=State.actualizar_filtro_ciudad_instituciones,
                                **ComponentStyle.FORM_SELECT,
                                width="300px",
                            ),
                            spacing="1",
                            margin_bottom="2em",
                        ),
                        
                        rx.cond(
                            State.instituciones_info,
                            rx.box(
                                rx.foreach(State.instituciones_info, render_institucion_card),
                                display="grid",
                                grid_template_columns="repeat(auto-fill, minmax(260px, 1fr))",
                                grid_auto_rows="auto",
                                gap="2em",
                                width="100%",
                                align_items="start",
                                justify_items="stretch",
                            ),
                            rx.text(
                                "No hay instituciones en la ciudad seleccionada.",
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
