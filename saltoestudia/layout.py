# saltoestudia/layout.py

import reflex as rx
from .state import State
from . import theme
from datetime import datetime
import os
from pathlib import Path

def navbar_icons_item(text: str, icon: str, url: str) -> rx.Component:
    return rx.link(
        rx.flex(
            rx.icon(tag=icon, size=16),
            rx.text(
                text, 
                size="3",
                font_family=theme.Typography.FONT_FAMILY,
                font_weight=theme.Typography.FONT_WEIGHTS["medium"],
                line_height="1",
                margin="0",
            ),
            align_items="center",
            gap="0.5rem",
        ), 
        href=url,
        color="white",
        _hover={
            "color": "#E3F2FD",
            "transform": "translateY(-1px)",
            "transition": "all 0.2s ease-in-out",
        },
        transition="all 0.2s ease-in-out",
        padding="0.4rem 0.6rem",
        border_radius="6px",
        height="2.2rem",
        display="flex",
        align_items="center",
    )

def navbar_icons_menu_item(text: str, icon: str, url: str) -> rx.Component:
    return rx.link(
        rx.hstack(
            rx.icon(icon, size=16), 
            rx.text(text, size="3", font_weight="medium")
        ), 
        href=url,
    )

def navbar_icons() -> rx.Component:
    # Header con altura fija y centrado perfecto
    return rx.box(
        # Desktop version
        rx.desktop_only(
            rx.flex(
                # Logo y título
                rx.flex(
                    rx.image(
                        src="/logo-redondo.png", 
                        width="2.2em",
                        height="2.2em",
                        border_radius="50%", 
                        cursor="pointer", 
                        on_click=rx.redirect("/"),
                        box_shadow="0 2px 8px rgba(0,0,0,0.1)",
                    ),
                    rx.heading(
                        "Salto Estudia", 
                        size="7",
                        font_family=theme.Typography.FONT_FAMILY,
                        font_weight=theme.Typography.FONT_WEIGHTS["semibold"], 
                        cursor="pointer", 
                        on_click=rx.redirect("/"),
                        color="white",
                        letter_spacing="-0.025em",
                        line_height="1",
                        margin="0",
                    ),
                    align_items="center",
                    gap="0.75rem",
                ),
                
                # Navegación
                rx.flex(
                    navbar_icons_item("Inicio", "view", "/"),
                    navbar_icons_item("Instituciones", "info", "/instituciones"),
                    navbar_icons_item("Buscador de cursos", "search", "/cursos"),
                    navbar_icons_item("Info", "info", "/info"),
                    align_items="center",
                    gap="0.25rem",
                    margin_right="0",
                ),
                
                justify="space-between",
                align_items="center",
                width="100%",
                height="100%",
                padding_left="1.5rem",
                padding_right="0.5rem",
            ),
        ),
        
        # Mobile version
        rx.mobile_and_tablet(
            rx.flex(
                # Logo y título móvil
                rx.flex(
                    rx.image(
                        src="/logo-redondo.png", 
                        width="2em", 
                        height="2em", 
                        border_radius="50%", 
                        cursor="pointer", 
                        on_click=rx.redirect("/")
                    ),
                    rx.heading(
                        "Salto Estudia", 
                        size="6", 
                        font_family=theme.Typography.FONT_FAMILY,
                        font_weight=theme.Typography.FONT_WEIGHTS["semibold"], 
                        cursor="pointer", 
                        on_click=rx.redirect("/"),
                        color="white",
                        line_height="1",
                        margin="0",
                    ),
                    align_items="center",
                    gap="0.5rem",
                ),
                
                # Botón menú
                rx.button(
                    "Menú", 
                    on_click=rx.redirect("/info"), 
                    size="2",
                    variant="ghost",
                    color="white",
                    font_family=theme.Typography.FONT_FAMILY,
                ),
                
                justify="space-between",
                align_items="center",
                width="100%",
                height="100%",
                padding_left="1.5rem",
                padding_right="0.5rem",
            ),
        ),
        
        # Estilos del contenedor principal
        bg="#004A99",
        width="100%",
        height="3.5rem",  # Altura fija para control total
        min_height="3.5rem",
        max_height="3.5rem",
        box_shadow="0 1px 3px rgba(0,0,0,0.1)",
        display="flex",
        align_items="center",
    )

def get_last_modification_date():
    """Obtiene la fecha de la última modificación de los archivos principales del proyecto."""
    project_root = Path(__file__).parent.parent  # Subir dos niveles desde layout.py
    python_files = list(project_root.rglob("*.py"))
    
    if not python_files:
        return datetime.now()
    
    # Encontrar el archivo con la fecha de modificación más reciente
    latest_file = max(python_files, key=lambda f: f.stat().st_mtime)
    latest_mtime = latest_file.stat().st_mtime
    
    return datetime.fromtimestamp(latest_mtime)

def footer():
    # Generar versión basada en la última modificación del código
    last_mod_date = get_last_modification_date()
    version = f"v{last_mod_date.year % 100:02d}.{last_mod_date.month:02d}"
    
    return rx.center(
        rx.box(
            rx.text(
                f"Salto Estudia {version} • Admin",
                font_size="10px",
                color="white",  # Texto blanco para buen contraste
                opacity="0.8",
                line_height="1",
                cursor="pointer",
                on_click=State.toggle_login_dialog,
                _hover={
                    "bg": "rgba(255,255,255,0.1)",
                    "opacity": "1",
                },
                padding_x="4px",
                border_radius="3px",
                transition="all 0.2s ease-in-out",
            ),
            bg="#004A99",  # Mismo azul sólido del header
            border_radius="8px",
            padding_x="10px",
            padding_y="2px",
            margin_top="auto",
            margin_bottom="6px",
            display="flex",
            align_items="center",
            justify_content="center",
            height="auto",
            min_height="18px",
        ),
        width="100%",
        bg="transparent",
    )

def login_dialog() -> rx.Component:
    """Diálogo de login para administradores."""
    return rx.cond(
        State.show_login_dialog,
        rx.box(
            rx.box(
                rx.vstack(
                    rx.heading("Acceso Administrador", size="7"),
                    rx.text("Ingresa tus credenciales para continuar."),
                    rx.vstack(
                        rx.input(
                            placeholder="tu@email.com",
                            on_change=State.set_login_correo,
                            type="email"
                        ),
                        rx.input(
                            placeholder="Tu contraseña",
                            on_change=State.set_login_password,
                            type="password"
                        ),
                        rx.cond(
                            State.login_error,
                            rx.text(State.login_error, color="red"),
                        ),
                        rx.hstack(
                            rx.button("Cancelar", on_click=State.toggle_login_dialog, variant="outline"),
                            rx.button("Ingresar", on_click=State.handle_login, variant="solid"),
                            spacing="3",
                        ),
                        spacing="4",
                        width="100%",
                    ),
                    spacing="4",
                    width="100%",
                ),
                bg=theme.Color.WHITE,
                padding="20px",
                border_radius="10px",
                box_shadow="xl",
                max_width="400px",
            ),
            position="fixed",
            top="0",
            left="0",
            width="100vw",
            height="100vh",
            bg="rgba(0,0,0,0.5)",
            display="flex",
            align_items="center",
            justify_content="center",
            z_index="1000",
        )
    )

def page_layout(*content):
    return rx.vstack(
        navbar_icons(),
        rx.box(
            *content, 
            padding="20px", 
            width="100%", 
            max_width="1400px", 
            flex_grow=1,
            bg=theme.Color.GRAY_100,  # Fondo gris para el contenido principal
        ),
        footer(),
        login_dialog(),
        min_height="100vh",
        width="100%",
        align_items="center",
        spacing="0",
        bg=theme.Color.GRAY_100,  # Fondo gris para toda la página
    )
