import reflex as rx
from ..state import obtener_instituciones  # Función que obtiene los datos desde la base de datos
from ..layout import page_layout          # Importar el layout con el header

def info():
    return page_layout(
        rx.vstack(
            rx.text("¿Y ahora, que estudio?", size="9", weight="bold", font_size="3xl", color_scheme="blue", high_contrast=True),
            rx.box(
                rx.text("""Esta herramienta está dirigida a estudiantes que terminan sus diferentes ciclos educativos y quieran informarse sobre que alternativas locales tienen disponibles para continuar su formación.""", 
                    white_space="pre-wrap", 
                    size="5",
                    text_align="center",
                    letter_spacing="1px"
                ),
                style={"max_width": 900},
            ),
            align_items="center",
            padding="40px",
            gap="40px",
        )
    )
