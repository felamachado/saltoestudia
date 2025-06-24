# saltoestudia/pages/index.py

import reflex as rx
from ..layout import page_layout
from .. import theme

# --- DECORADOR AÑADIDO ---
# Esta línea es la que registra la función como la página de inicio.
@rx.page(route="/", title="Inicio | Salto Estudia")
def index() -> rx.Component:
    return page_layout(
        rx.vstack(
            rx.heading("¡Bienvenidos!", size="9", color=theme.Color.BLUE_300),
            rx.text(
                "En Salto Estudia vas a poder encontrar la oferta educativa local que mejor se adapta a vos.",
                size="4",
                color=theme.Color.GRAY_900,  # Texto claro sobre fondo oscuro
                text_align="center",
            ),
            rx.hstack(
                tarjeta("Instituciones", "Conocé las instituciones educativas.", "info", "/instituciones"),
                tarjeta("Cursos", "Explorá todos los cursos disponibles.", "search", "/cursos"),
                spacing="6",
            ),
            align_items="center",
            padding="40px",
            spacing="8",
        )
    )

def tarjeta(titulo, descripcion, icono, link=None):
    return rx.box(
        rx.vstack(
            rx.icon(tag=icono, size=50, color=theme.Color.BLUE_300),
            rx.text(
                titulo, 
                font_weight="bold", 
                size="6", 
                color=theme.Color.GRAY_900,
                text_align="center"
            ),
            rx.text(
                descripcion, 
                text_align="center", 
                color=theme.Color.GRAY_700,
                size="4",
                line_height="1.5"
            ),
            align_items="center",
            justify="between",  # Cambiado de "space-evenly" a "between"
            spacing="3",
            height="100%",  # Ocupa toda la altura del contenedor
        ),
        padding="32px",
        shadow="2xl",
        border_radius="12px",
        cursor="pointer",
        on_click=(rx.redirect(link) if link else None),
        bg=theme.Color.DARK_CARD,  # Fondo muy oscuro para las tarjetas
        border=f"1px solid {theme.Color.GRAY_500}",  # Borde gris medio
        width="300px",
        height="280px",  # ALTURA FIJA - esto iguala ambas tarjetas
        _hover={
            "shadow": "2xl",
            "transform": "scale(1.05)",
            "transition": "all 0.2s ease-in-out",
            "border_color": theme.Color.BLUE_500,  # Borde azul más intenso en hover
            "bg": theme.Color.GRAY_300,  # Fondo ligeramente más claro en hover
        }
    )
