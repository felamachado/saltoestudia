import reflex as rx
from ..database import obtener_instituciones
from ..layout import page_layout
from ..state import State

class DialogState(rx.State):
    opened: bool = False
    selected_institution: dict = {}

    def dialog_open(self, institution):
        self.opened = True
        self.selected_institution = institution

    def dialog_close(self):
        self.opened = False

    def count_opens(self, value: bool):
        self.opened = value

    def ver_oferta(self):
        State.actualizar_institución_seleccionada(self.selected_institution["nombre"])
        return rx.redirect("/cursos")


def instituciones():
    # Obtener los datos desde la base de datos
    instituciones = obtener_instituciones()

    # Crear una lista de tarjetas con el diálogo para cada institución
    tarjetas = [
        rx.card(
            rx.vstack(
                rx.image(src="/logoutu.png", width="100px", height="auto"),
                rx.text(institucion["nombre"], font_weight="bold"),
                align_items="center"
            ),
            padding="10px",
            shadow="lg",
            border_radius="10px",
            background_color="transparent",
            margin_bottom="20px",
            cursor="pointer",  # Change cursor to pointer to indicate it's clickable
            on_click=lambda institution=institucion: DialogState.dialog_open(institution)
        )
        for institucion in instituciones
    ]

    # Retornar el contenido dentro del layout
    return page_layout(
        rx.center(
            rx.vstack(
                rx.hstack(
                    *tarjetas,
                    gap="20px",
                    padding="20px"
                ),
                template_columns="repeat(auto-fill, minmax(300px, 1fr))",
                gap="20px",
                padding="20px"
            )
        ),
        rx.dialog.root(
            rx.dialog.content(
            rx.dialog.title(DialogState.selected_institution["nombre"]),
            rx.dialog.description(
                rx.text(
                    rx.text.strong("Teléfono: "),
                    f"{DialogState.selected_institution['telefono']}",
                ),
                rx.text(
                    rx.text.strong("Dirección: "),
                    f"{DialogState.selected_institution['direccion']}",
                ),
                rx.text(
                    rx.text.strong("Correo: "),
                    f"{DialogState.selected_institution['correo']}",
                ),
            ),
            rx.flex(
                rx.dialog.close(
                    rx.button(
                        "Cerrar",
                        variant="soft",
                        color_scheme="gray",
                        cursor="default"
                    ),
                ),
                rx.dialog.close(
                    rx.button("Ver oferta"),
                        cursor="pointer",
                        on_click=DialogState.ver_oferta  # Llamar a la función personalizada
                        #on_click=rx.redirect("/cursos"),
                ),
                spacing="3",
                margin_top="16px",
                #justify="end",
            )
    ),
    open=DialogState.opened,
    on_open_change=DialogState.count_opens,
)
    )