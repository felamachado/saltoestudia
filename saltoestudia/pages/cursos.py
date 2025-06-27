# saltoestudia/pages/cursos.py

import reflex as rx
from reflex_ag_grid import ag_grid
from ..layout import page_layout
from ..state import State
from .. import theme
from ..theme import ComponentStyle, create_course_table_header, create_course_table_cell, create_custom_dropdown_css, ButtonStyle
from ..constants import CursosConstants

def render_curso_card_mobile_public(curso: dict) -> rx.Component:
    """Renderiza una tarjeta de curso para móvil en la página pública."""
    return rx.box(
        rx.vstack(
            # Título del curso
            rx.heading(
                curso["nombre"],
                size="4",
                color=theme.Color.BLUE_300,
                font_family=theme.Typography.FONT_FAMILY,
                font_weight=theme.Typography.FONT_WEIGHTS["bold"],
                margin_bottom="8px",
                line_height="1.3",
            ),
            
            # Información del curso
            rx.vstack(
                rx.hstack(
                    rx.text("Nivel:", font_weight="bold", color=theme.Color.GRAY_900, font_size="3"),
                    rx.text(curso["nivel"], color=theme.Color.GRAY_700, font_size="3"),
                    spacing="2",
                    align="center",
                    justify="start",
                ),
                rx.hstack(
                    rx.text("Duración:", font_weight="bold", color=theme.Color.GRAY_900, font_size="3"),
                    rx.text(
                        rx.cond(
                            curso["duracion_numero"],
                            f"{curso['duracion_numero']} {curso['duracion_unidad']}",
                            "N/A"
                        ),
                        color=theme.Color.GRAY_700,
                        font_size="3",
                    ),
                    spacing="2",
                    align="center",
                    justify="start",
                ),
                rx.hstack(
                    rx.text("Requisitos:", font_weight="bold", color=theme.Color.GRAY_900, font_size="3"),
                    rx.text(curso["requisitos_ingreso"], color=theme.Color.GRAY_700, font_size="3"),
                    spacing="2",
                    align="center",
                    justify="start",
                ),
                rx.hstack(
                    rx.text("Institución:", font_weight="bold", color=theme.Color.GRAY_900, font_size="3"),
                    rx.text(curso["institucion"], color=theme.Color.GRAY_700, font_size="3"),
                    spacing="2",
                    align="center",
                    justify="start",
                ),
                rx.cond(
                    curso["informacion"],
                    rx.vstack(
                        rx.text("Información:", font_weight="bold", color=theme.Color.GRAY_900, font_size="3"),
                        rx.text(
                            curso["informacion"],
                            color=theme.Color.GRAY_700,
                            font_size="2",
                            line_height="1.4",
                        ),
                        align_items="start",
                        spacing="1",
                        width="100%",
                    ),
                ),
                spacing="3",
                align_items="start",
                width="100%",
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

def cursos_filters_desktop() -> rx.Component:
    """Filtros para versión desktop."""
    return rx.box(
        # Filtros de búsqueda
        rx.vstack(
            # Primera fila de filtros
            rx.hstack(
                rx.vstack(
                    rx.text(
                        "Nivel:", 
                        font_weight=theme.Typography.FONT_WEIGHTS["semibold"], 
                        font_size="2",
                        color=theme.Color.GRAY_900,
                        font_family=theme.Typography.FONT_FAMILY,
                    ),
                    rx.select(
                        ["Todos"] + CursosConstants.NIVELES,
                        placeholder="Seleccionar...",
                        value=rx.cond(State.nivel_seleccionado == "", "Todos", State.nivel_seleccionado),
                        on_change=State.actualizar_nivel_seleccionado,
                        width="100%",
                        **ComponentStyle.FORM_SELECT,
                    ),
                    spacing="1",
                    align="start",
                    width=["100%", "48%", "23%", "23%"],
                ),
                rx.vstack(
                    rx.text(
                        "Req. Ingreso:", 
                        font_weight=theme.Typography.FONT_WEIGHTS["semibold"], 
                        font_size="2",
                        color=theme.Color.GRAY_900,
                        font_family=theme.Typography.FONT_FAMILY,
                    ),
                    rx.select(
                        ["Todos"] + CursosConstants.REQUISITOS_INGRESO,
                        placeholder="Seleccionar...",
                        value=rx.cond(State.requisito_seleccionado == "", "Todos", State.requisito_seleccionado),
                        on_change=State.actualizar_requisito_seleccionado,
                        width="100%",
                        **ComponentStyle.FORM_SELECT,
                    ),
                    spacing="1",
                    align="start",
                    width=["100%", "48%", "23%", "23%"],
                ),
                rx.vstack(
                    rx.text(
                        "Institución:", 
                        font_weight=theme.Typography.FONT_WEIGHTS["semibold"], 
                        font_size="2",
                        color=theme.Color.GRAY_900,
                        font_family=theme.Typography.FONT_FAMILY,
                    ),
                    rx.select(
                        State.instituciones_nombres,
                        placeholder="Seleccionar...",
                        value=rx.cond(State.institucion_seleccionada == "", "Todos", State.institucion_seleccionada),
                        on_change=State.actualizar_institución_seleccionada,
                        width="100%",
                        **ComponentStyle.FORM_SELECT,
                    ),
                    spacing="1",
                    align="start",
                    width=["100%", "48%", "23%", "23%"],
                ),
                rx.box(
                    rx.button(
                        "Limpiar Filtros",
                        on_click=State.limpiar_filtros,
                        **ButtonStyle.secondary(),
                        width="100%",
                    ),
                    width=["100%", "48%", "23%", "23%"],
                    align_self="end",
                ),
                justify="between",
                spacing="2",
                width="100%",
                wrap="wrap",
                align_items="end",
            ),
            
            spacing="3",
            width="100%",
        ),
        width="100%",
        margin_x="auto",
        padding_x="0.5em",
        margin_bottom="1em",
    )

def cursos_filters_mobile() -> rx.Component:
    """Filtros para versión móvil."""
    return rx.vstack(
        rx.vstack(
            rx.text(
                "Nivel:", 
                font_weight=theme.Typography.FONT_WEIGHTS["semibold"], 
                color=theme.Color.GRAY_900,
                font_family=theme.Typography.FONT_FAMILY,
                font_size="3",
            ),
            rx.select(
                ["Todos"] + CursosConstants.NIVELES,
                placeholder="Seleccionar nivel...",
                value=rx.cond(State.nivel_seleccionado == "", "Todos", State.nivel_seleccionado),
                on_change=State.actualizar_nivel_seleccionado,
                width="100%",
                **ComponentStyle.FORM_SELECT,
            ),
            spacing="2",
            align="start",
            width="100%",
        ),
        rx.vstack(
            rx.text(
                "Requisitos de Ingreso:", 
                font_weight=theme.Typography.FONT_WEIGHTS["semibold"], 
                color=theme.Color.GRAY_900,
                font_family=theme.Typography.FONT_FAMILY,
                font_size="3",
            ),
            rx.select(
                ["Todos"] + CursosConstants.REQUISITOS_INGRESO,
                placeholder="Seleccionar requisitos...",
                value=rx.cond(State.requisito_seleccionado == "", "Todos", State.requisito_seleccionado),
                on_change=State.actualizar_requisito_seleccionado,
                width="100%",
                **ComponentStyle.FORM_SELECT,
            ),
            spacing="2",
            align="start",
            width="100%",
        ),
        rx.vstack(
            rx.text(
                "Institución:", 
                font_weight=theme.Typography.FONT_WEIGHTS["semibold"], 
                color=theme.Color.GRAY_900,
                font_family=theme.Typography.FONT_FAMILY,
                font_size="3",
            ),
            rx.select(
                State.instituciones_nombres,
                placeholder="Seleccionar institución...",
                value=rx.cond(State.institucion_seleccionada == "", "Todos", State.institucion_seleccionada),
                on_change=State.actualizar_institución_seleccionada,
                width="100%",
                **ComponentStyle.FORM_SELECT,
            ),
            spacing="2",
            align="start",
            width="100%",
        ),
        rx.button(
            "Limpiar Filtros",
            on_click=State.limpiar_filtros,
            **ButtonStyle.secondary(),
            width="100%",
        ),
        spacing="4",
        width="100%",
        padding="1em",
    )

def cursos_content_desktop() -> rx.Component:
    """Contenido de cursos para desktop."""
    return rx.vstack(
        # Título principal
        rx.heading(
            "Buscador de Cursos", 
            size="8", 
            color=theme.Color.BLUE_300,
            font_family=theme.Typography.FONT_FAMILY,
            font_weight=theme.Typography.FONT_WEIGHTS["bold"],
            margin_bottom="0.5em", 
            text_align="center"
        ),
        # Subtítulo
        rx.text(
            "Encuentra los cursos que mejor se adapten a tus necesidades.", 
            size="4",
            color=theme.Color.GRAY_900,
            font_family=theme.Typography.FONT_FAMILY,
            text_align="center",
            margin_bottom="1.5em",
        ),
        
        # Filtros desktop
        rx.desktop_only(cursos_filters_desktop()),
        rx.mobile_and_tablet(cursos_filters_mobile()),
        
        # Tabla básica de Reflex
        rx.cond(
            State.cursos,
            rx.table.root(
                rx.table.header(
                    rx.table.row(
                        rx.table.cell("Nombre"),
                        rx.table.cell("Nivel"),
                        rx.table.cell("Duración"),
                        rx.table.cell("Requisitos"),
                        rx.table.cell("Institución"),
                        rx.table.cell("Información"),
                    )
                ),
                rx.table.body(
                    rx.foreach(
                        State.cursos,
                        lambda curso: rx.table.row(
                            rx.table.cell(curso["nombre"]),
                            rx.table.cell(curso["nivel"]),
                            rx.table.cell(f"{curso['duracion_numero']} {curso['duracion_unidad']}"),
                            rx.table.cell(curso["requisitos_ingreso"]),
                            rx.table.cell(curso["institucion"]),
                            rx.table.cell(curso["informacion"]),
                        )
                    )
                ),
                width="100%",
            ),
            rx.box(
                rx.text(
                    "No se encontraron cursos con los filtros seleccionados.",
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
        
        align_items="stretch",
        padding="40px",
        spacing="6",
        width="100%",
    )

def cursos_content_mobile() -> rx.Component:
    """Contenido de cursos para móvil."""
    return rx.vstack(
        # Título principal móvil
        rx.heading(
            "Buscador de Cursos", 
            size="7", 
            color=theme.Color.BLUE_300,
            font_family=theme.Typography.FONT_FAMILY,
            font_weight=theme.Typography.FONT_WEIGHTS["bold"],
            text_align="center",
            margin_bottom="8px"
        ),
        # Subtítulo móvil
        rx.text(
            "Encuentra los cursos que mejor se adapten a tus necesidades.", 
            size="3",
            color=theme.Color.GRAY_900,
            font_family=theme.Typography.FONT_FAMILY,
            text_align="center",
            line_height="1.4",
            margin_bottom="1em",
        ),
        
        # Filtros móvil
        rx.mobile_and_tablet(cursos_filters_mobile()),
        
        # Contenido de cursos en tarjetas - OPTIMIZADO COLD START
        rx.cond(
            State.cursos_cache_loaded,
            # Mostrar contenido cuando los datos están cargados
            rx.cond(
                State.cursos,
                # Mostrar tarjetas cuando hay datos
                rx.vstack(
                    rx.foreach(State.cursos, render_curso_card_mobile_public),
                    spacing="0",
                    width="100%",
                ),
                # Mostrar mensaje cuando no hay datos
                rx.box(
                    rx.text(
                        "No se encontraron cursos con los filtros seleccionados.",
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
            # Mostrar skeleton mientras carga por primera vez
            cursos_skeleton_mobile()
        ),
        
        align_items="stretch",
        padding="1em",
        spacing="4",
        width="100%",
    )

@rx.page(route="/cursos", title="Cursos | Salto Estudia", on_load=State.cargar_datos_cursos_page)
def cursos() -> rx.Component:
    return page_layout(
        create_custom_dropdown_css(),
        rx.desktop_only(cursos_content_desktop()),
        rx.mobile_and_tablet(cursos_content_mobile()),
    )

def render_curso_row_public(curso_data: list) -> rx.Component:
    """Renderiza una fila de la tabla de cursos para la página pública."""
    return rx.table.row(
        create_course_table_cell(curso_data[0]),  # Nombre
        create_course_table_cell(curso_data[1]),  # Nivel
        create_course_table_cell(curso_data[2]),  # Duración
        create_course_table_cell(curso_data[3]),  # Requisitos
        create_course_table_cell(curso_data[4]),  # Institución
        create_course_table_cell(curso_data[5]),  # Información
        **ComponentStyle.COURSE_TABLE_ROW_HOVER,
    )

def cursos_skeleton_desktop() -> rx.Component:
    """Skeleton screen para desktop mientras cargan los datos."""
    return rx.vstack(
        # Título skeleton
        rx.skeleton(
            rx.box(height="40px", width="300px"),
            loading=True,
            margin_bottom="0.5em"
        ),
        # Subtítulo skeleton
        rx.skeleton(
            rx.box(height="20px", width="500px"),
            loading=True,
            margin_bottom="1.5em"
        ),
        # Filtros skeleton
        rx.hstack(
            rx.skeleton(rx.box(height="40px", width="120px"), loading=True),
            rx.skeleton(rx.box(height="40px", width="140px"), loading=True),
            rx.skeleton(rx.box(height="40px", width="130px"), loading=True),
            rx.skeleton(rx.box(height="40px", width="110px"), loading=True),
            spacing="2",
            margin_bottom="1em",
        ),
        # Grid skeleton
        rx.skeleton(
            rx.box(height="500px", width="100%"),
            loading=True,
        ),
        align_items="center",
        padding="40px",
        spacing="6",
        width="100%",
    )

def cursos_skeleton_mobile() -> rx.Component:
    """Skeleton screen para móvil mientras cargan los datos."""
    return rx.vstack(
        # Título skeleton móvil
        rx.skeleton(
            rx.box(height="32px", width="250px"),
            loading=True,
            margin_bottom="8px"
        ),
        # Subtítulo skeleton móvil
        rx.skeleton(
            rx.box(height="16px", width="350px"),
            loading=True,
            margin_bottom="1em"
        ),
        # Filtros skeleton móvil
        rx.vstack(
            rx.skeleton(rx.box(height="50px", width="100%"), loading=True),
            rx.skeleton(rx.box(height="50px", width="100%"), loading=True),
            rx.skeleton(rx.box(height="50px", width="100%"), loading=True),
            rx.skeleton(rx.box(height="40px", width="100%"), loading=True),
            spacing="4",
            width="100%",
            margin_bottom="1em",
        ),
        # Tarjetas skeleton
        rx.vstack(
            rx.skeleton(rx.box(height="150px", width="100%"), loading=True),
            rx.skeleton(rx.box(height="150px", width="100%"), loading=True),
            rx.skeleton(rx.box(height="150px", width="100%"), loading=True),
            spacing="3",
            width="100%",
        ),
        align_items="stretch",
        padding="1em",
        spacing="4",
        width="100%",
    )

