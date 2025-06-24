# saltoestudia/pages/cursos.py

import reflex as rx
from reflex_ag_grid import ag_grid
from ..layout import page_layout
from ..state import State
from .. import theme
from ..theme import ComponentStyle, create_course_table_header, create_course_table_cell, create_custom_dropdown_css, ButtonStyle
from ..constants import CursosConstants

@rx.page(route="/cursos", title="Cursos | Salto Estudia", on_load=State.cargar_datos_cursos_page)
def cursos() -> rx.Component:
    return page_layout(
        create_custom_dropdown_css(),
        rx.vstack(
            # Título principal
            rx.heading(
                "Buscador de Cursos", 
                size="8", 
                color=theme.Color.BLUE_300,  # accent
                font_family=theme.Typography.FONT_FAMILY,
                font_weight=theme.Typography.FONT_WEIGHTS["bold"],
                margin_bottom="0.5em", 
                text_align="center"
            ),
            # Subtítulo
            rx.text(
                "Encuentra los cursos que mejor se adapten a tus necesidades.", 
                size="4",
                color=theme.Color.GRAY_900,  # on_background
                font_family=theme.Typography.FONT_FAMILY,
                text_align="center",
                margin_bottom="1.5em",
            ),
            
            # Contenedor para centrar y limitar el ancho de los filtros
            rx.box(
                # Filtros de búsqueda
                rx.vstack(
                    # Primera fila de filtros
                    rx.hstack(
                        rx.vstack(
                            rx.text(
                                "Nivel:", 
                                font_weight=theme.Typography.FONT_WEIGHTS["semibold"], 
                                font_size="2",
                                color=theme.Color.GRAY_900,  # on_background
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
                                color=theme.Color.GRAY_900,  # on_background
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
                                color=theme.Color.GRAY_900,  # on_background
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
                            align_self="end",  # Alinear al final del contenedor padre
                        ),
                        justify="between",
                        spacing="2",
                        width="100%",
                        wrap="wrap",
                        align_items="end",  # Alinear todos los elementos al final
                    ),
                    
                    spacing="3",
                    width="100%",
                ),
                width="100%",
                margin_x="auto",
                padding_x="0.5em",
                margin_bottom="1em",
            ),
            
            # AG Grid para cursos
            rx.cond(
                State.cursos,
                # Mostrar AG Grid cuando hay datos
                ag_grid(
                    id="cursos_grid",
                    row_data=State.cursos,
                    column_defs=[
                        {
                            "headerName": "Nombre", 
                            "field": "nombre", 
                            "sortable": True,
                            "flex": 3,
                            "minWidth": 200,
                            "maxWidth": 350
                        },
                        {
                            "headerName": "Nivel", 
                            "field": "nivel", 
                            "sortable": True,
                            "width": 120,
                            "suppressSizeToFit": False
                        },
                        {
                            "headerName": "Duración", 
                            "field": "duracion_numero", 
                            "sortable": True,
                            "width": 80,
                            "headerTooltip": "Duración en números"
                        },
                        {
                            "headerName": "Unidad", 
                            "field": "duracion_unidad", 
                            "sortable": True,
                            "width": 90,
                            "headerTooltip": "Unidad de tiempo"
                        },
                        {
                            "headerName": "Requisitos", 
                            "field": "requisitos_ingreso", 
                            "sortable": True,
                            "flex": 2,
                            "minWidth": 140,
                            "maxWidth": 200
                        },
                        {
                            "headerName": "Institución", 
                            "field": "institucion", 
                            "sortable": True,
                            "flex": 2,
                            "minWidth": 150,
                            "maxWidth": 220
                        },
                        {
                            "headerName": "Información", 
                            "field": "informacion", 
                            "sortable": True,
                            "flex": 3,
                            "minWidth": 200,
                            "wrapText": True,
                            "autoHeight": True,
                            "cellRenderer": "agTextCellRenderer"
                        }
                    ],
                    theme="alpine",
                    width="100%",
                    height="500px",
                    pagination=True,
                    pagination_page_size=25,
                    default_col_def={
                        "resizable": True,
                        "sortable": True,
                        "filter": False,
                        "suppressMovable": True,
                        "suppressMenu": True
                    },
                    grid_options={
                        "suppressHorizontalScroll": True,
                        "suppressColumnVirtualisation": True,
                        "domLayout": "normal",
                        "rowHeight": 45,
                        "headerHeight": 30,
                        "animateRows": True,
                        "enableCellTextSelection": True,
                        "suppressMenuHide": True,
                        "alwaysShowHorizontalScroll": False,
                        "alwaysShowVerticalScroll": False
                    }
                ),
                # Mostrar mensaje cuando no hay datos
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
            padding="40px",  # padding normal
            spacing="6",     # spacing normal
            width="100%",
        )
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

