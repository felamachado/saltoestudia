import reflex as rx
from ..state import obtener_instituciones  # Función que obtiene los datos desde la base de datos
from ..layout import page_layout          # Importar el layout con el header
from ..database import obtener_instituciones  # Importa directamente desde database.py

def index():
    return page_layout(
        rx.vstack(
            rx.text("¡Bienvenidos!", size="9", weight="bold", font_size="3xl", color_scheme="blue", high_contrast=True),
            rx.text("En ", rx.text.strong("Salto Estudia")," vas a poder encontrar la oferta educativa ", rx.text.strong("local "), "que mejor se adapta a vos.", size="6"),
            #rx.text("Nuestra Oferta", font_size="2xl", font_weight="bold"),
            rx.hstack(
                tarjeta("Instituciones", "Conocé las instituciones.", "university", "/instituciones"),
                tarjeta("Cursos", "Explorá los cursos disponibles.", "search", "/cursos"),
                gap="20px",
            ),
            align_items="center",
            padding="40px",
            gap="40px",
        )
    )

def tarjeta(titulo, descripcion, icono, link=None):
    return rx.card(
        rx.icon(icono, size=40, margin_bottom="10px"),
        rx.text(titulo, font_weight="bold"),
        rx.text(descripcion),
        padding="20px",
        shadow="lg",
        border_radius="10px",
        align_items="center",
        cursor="pointer",
        on_click=(rx.redirect(link) if link else None),
        _hover={
            "background_color": "#0A2342",  # Color de fondo al pasar el cursor
            "color": "#87CEEB",
            "shadow": "xl",
            "transform": "scale(1.10)",  # Ligeramente más grande en hover
            "transition": "all 0.3s ease-in-out"  # Suaviza la transición
        }
    )