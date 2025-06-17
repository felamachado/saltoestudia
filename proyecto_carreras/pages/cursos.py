import reflex as rx
from ..layout import page_layout
from ..state import State

def cursos():
    # Define columns for the table
    columns = ["Nombre", "Nivel", "Duración", "Requisitos de Ingreso", "Institución", "Información"]


    # Return the layout with the table
    return page_layout(
        rx.hstack(
            rx.hstack(
                rx.heading("Nivel:"),
                rx.select(
                items=State.niveles,
                placeholder="Selecciona nivel",
                on_change=State.actualizar_nivel_seleccionado,
                width= "120px"
                ),
                width="15%",
            ),         
            rx.hstack(
                rx.heading("Duración:"),
                rx.select(
                items=["Todos", "1", "2", "3"],
                placeholder="Selecciona duración",
                on_change=State.actualizar_duracion_seleccionada,
                width= "120px",
                ),
                width="20%",
            ),
            rx.hstack(
                rx.heading("Req. Ingreso:"),
                rx.select(
                items=State.requisitos,
                placeholder="Selecciona requisito",
                on_change=State.actualizar_requisito_seleccionado,
                width= "250px"
                ),
                width="30%",
            ),
            rx.hstack(
                rx.heading("Institución:"),
                rx.select(
                items=State.instituciones_nombres,
                placeholder="Selecciona Institución",
                on_change=State.actualizar_institución_seleccionada,
                width= "250px"
                ),
                width="30%",
            ),
            align="center",
            justify="center",
            width="100%"
        ),  

        rx.box(height="20px"),
        rx.divider(mb="4"),
        rx.box(height="20px"),

        rx.box(
            
            rx.data_table(
                data=State.tabla_cursos,
                columns=columns,
                pagination=True,
                search=False,
                sort=True,
                resizable=True,
                on_mount=[State.cargar_cursos, State.cargar_niveles, State.cargar_requisitos, State.cargar_instituciones_nombres],
                style={"table-layout": "auto"},
            ),
        )
    )