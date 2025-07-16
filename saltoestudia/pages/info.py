import reflex as rx
from ..layout import page_layout
from .. import theme
from ..theme import Typography

@rx.page(route="/info", title="Info | Salto Estudia")
def info() -> rx.Component:
    return page_layout(
        rx.vstack(
            # Contenedor principal centrado con max-width
            rx.box(
                rx.vstack(
                    # Título principal con jerarquía visual clara
                    rx.heading(
                        "¿Y ahora, qué estudio?",
                        size="9",
                        color=theme.Color.GRAY_900,  # on_background
                        font_family=Typography.FONT_FAMILY,
                        font_weight=Typography.FONT_WEIGHTS["bold"],
                        text_align="center",
                        margin_bottom="1em",
                        line_height="1.2",
                    ),
                    
                    # Párrafo introductorio con tipografía mediana
                    rx.text(
                        "Esta herramienta está dirigida a estudiantes que terminan sus diferentes "
                        "ciclos educativos y quieran informarse sobre qué alternativas locales "
                        "tienen disponibles para continuar su formación.",
                        size="5",
                        color=theme.Color.GRAY_700,  # on_background-subtle
                        font_family=Typography.FONT_FAMILY,
                        font_weight=Typography.FONT_WEIGHTS["normal"],
                        text_align="center",
                        line_height="1.6",
                        max_width="600px",
                    ),
                    
                    spacing="6",
                    align_items="center",
                    width="100%",
                ),
                # Centrado horizontal y vertical con max-width razonable
                max_width="800px",
                width="90%",
                margin_x="auto",
                padding_y="4em",  # Márgenes generosos arriba y abajo
            ),
            # Centrado vertical en el viewport
            min_height="70vh",
            justify_content="center",
            align_items="center",
            width="100%",
        )
    )
