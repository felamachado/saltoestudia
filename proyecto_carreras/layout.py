import reflex as rx
from .state import State

def navbar_icons() -> rx.Component:
    return rx.box(
        rx.desktop_only(
            rx.hstack(
                rx.hstack(
                    rx.image(
                        src="/logo-redondo.png",
                        width="2.25em",
                        height="auto",
                        border_radius="25%",
                        cursor="pointer",
                        on_click=rx.redirect("/"),
                    ),
                    rx.heading(
                        "Salto Estudia", size="7", weight="bold",
                        cursor="pointer",
                        on_click=rx.redirect("/"),
                    ),
                    align_items="center",
                ),
                rx.hstack(
                    navbar_icons_item(
                            "Inicio", "home", "/"
                        ),
                    navbar_icons_item("Instituciones", "university", "/instituciones"),
                    navbar_icons_item(
                        "Buscador de cursos", "search", "/cursos"
                    ),
                    navbar_icons_item(
                        "Info", "info", "/info"
                    ),
                    spacing="6",
                ),
                justify="between",
                align_items="center",
            ),
        ),
        rx.mobile_and_tablet(
            rx.hstack(
                rx.hstack(
                    rx.image(
                        src="/logo-redondo.png",
                        width="2em",
                        height="auto",
                        border_radius="25%",
                        cursor="pointer",
                        on_click=rx.redirect("/"),
                    ),
                    rx.heading(
                        "Salto Estudia", size="6", weight="bold",   
                        cursor="pointer",
                        on_click=rx.redirect("/"),
                    ),
                    align_items="center",
                ),
                rx.menu.root(
                    rx.menu.trigger(
                        rx.icon("menu", size=30)
                    ),
                    rx.menu.content(
                        navbar_icons_menu_item(
                            "Inicio", "home", "/"
                        ),
                        navbar_icons_menu_item(
                            "Instituciones", "university", "/instituciones"
                        ),
                        navbar_icons_menu_item(
                            "Buscador de cursos", "search", "/cursos"
                        ),
                        navbar_icons_menu_item(
                            "Info", "info", "/info"
                        ),
                    ),
                    justify="end",
                ),
                justify="between",
                align_items="center",
            ),
        ),
        bg=rx.color("accent", 3),
        padding="1em",
        # position="fixed",
        # top="0px",
        # z_index="5",
        width="100%",
    )

# Definir el Header usando clases de Bootstrap
def navbar_icons_item(
    text: str, icon: str, url: str
) -> rx.Component:
    return rx.link(
        rx.hstack(
            rx.icon(icon),
            rx.text(text, size="4", weight="medium"),
        ),
        href=url,
    )


def navbar_icons_menu_item(
    text: str, icon: str, url: str
) -> rx.Component:
    return rx.link(
        rx.hstack(
            rx.icon(icon, size=16),
            rx.text(text, size="3", weight="medium"),
        ),
        href=url,
    )
 
def footer():
    return rx.box(
        rx.text("Vers. 24.11", font_size="11px"),  # Muestra el contador en el footer
        padding="1px",
        color="white",
        text_align="center",
        margin_top="auto",
    )

# Función para envolver cada página en un layout con el header
def page_layout(*content):
    return rx.vstack(
        navbar_icons(),  # Añadir el header
        rx.box(content, padding="20px"),  # Contenido de cada página
        footer(),  # Añadir el footer con el contador de visitas
        min_height="100vh",
        width="100%",
        align="center"
    )
