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
    """HEADER COMPLETAMENTE NUEVO - DISEÑO SIMPLE Y DIRECTO"""
    return rx.box(
        # === VERSIÓN DESKTOP ===
        rx.desktop_only(
            rx.hstack(
                # === LADO IZQUIERDO: LOGO + TÍTULO ===
                rx.hstack(
                    rx.image(
                        src="/logo-redondo.png",
                        width="40px",
                        height="40px", 
                        border_radius="50%",
                        cursor="pointer",
                        on_click=rx.redirect("/"),
                    ),
                    rx.text(
                        "Salto Estudia",
                        font_size="22px",
                        font_weight="600",
                        color="white",
                        cursor="pointer",
                        on_click=rx.redirect("/"),
                        font_family=theme.Typography.FONT_FAMILY,
                        # CENTRADO VERTICAL SIMPLE
                        line_height="40px",  # Igual a la altura del logo
                        margin="0",
                        padding="0",
                    ),
                    spacing="12px",
                    align="center",
                ),
                
                # === LADO DERECHO: NAVEGACIÓN ===  
                rx.hstack(
                    navbar_icons_item("Inicio", "view", "/"),
                    navbar_icons_item("Instituciones", "info", "/instituciones"), 
                    navbar_icons_item("Buscador de cursos", "search", "/cursos"),
                    navbar_icons_item("Info", "info", "/info"),
                    spacing="8px",
                    align="center",
                ),
                
                # === DISTRIBUCIÓN HORIZONTAL PERFECTA ===
                justify="between",  # Separación máxima izquierda-derecha
                align="center",     # Centrado vertical
                width="100%",
                padding_x="24px",
                height="56px",      # Altura explícita del header
                min_height="56px",  # Asegurar altura mínima
            )
        ),
        
        # === VERSIÓN MÓVIL ===
        rx.mobile_and_tablet(
            rx.hstack(
                # Logo + título móvil
                rx.hstack(
                    rx.image(
                        src="/logo-redondo.png",
                        width="32px", 
                        height="32px",
                        border_radius="50%",
                        cursor="pointer",
                        on_click=rx.redirect("/"),
                    ),
                    rx.text(
                        "Salto Estudia",
                        font_size="18px",
                        font_weight="600", 
                        color="white",
                        cursor="pointer",
                        on_click=rx.redirect("/"),
                        font_family=theme.Typography.FONT_FAMILY,
                        # CENTRADO VERTICAL SIMPLE MÓVIL
                        line_height="32px",  # Igual a la altura del logo móvil
                        margin="0",
                        padding="0",
                    ),
                    spacing="8px",
                    align="center",
                ),
                
                # Botón menú móvil
                rx.button(
                    "☰",
                    on_click=rx.redirect("/info"),
                    bg="transparent",
                    color="white",
                    font_size="20px",
                    border="none",
                    cursor="pointer",
                ),
                
                # === DISTRIBUCIÓN HORIZONTAL MÓVIL ===
                justify="between",    # Separación máxima izquierda-derecha
                align="center",       # Centrado vertical
                width="100%",
                padding_x="16px",
                height="56px",        # Altura explícita del header
                min_height="56px",    # Asegurar altura mínima
            )
        ),
        
        # === ESTILOS DEL CONTENEDOR PRINCIPAL ===
        background="#004A99",
        width="100%", 
        height="56px",
        min_height="56px",
        position="sticky",
        top="0",
        z_index="1000",
        box_shadow="0 2px 4px rgba(0,0,0,0.1)",
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
    """
    Diálogo de login para administradores desde el header.
    
    Modal que aparece cuando se hace clic en el footer. Utiliza los estilos
    centralizados del tema para mantener consistencia visual con el resto
    del sistema.
    
    COLORES APLICADOS:
    - Fondo del modal: DARK_CARD (tema oscuro consistente)
    - Campos de input: FORM_INPUT (estilo centralizado)
    - Botones: ButtonStyle.primary() y secondary()
    - Textos: GRAY_900 para títulos, GRAY_700 para contenido
    
    UTILIZADO EN:
    - Header footer cuando se hace clic en "Admin"
    - Permite acceso rápido sin ir a /login
    - Redirige automáticamente a /admin tras autenticación exitosa
    """
    return rx.cond(
        State.show_login_dialog,
        rx.box(
            rx.box(
                rx.vstack(
                    # === HEADER DEL MODAL ===
                    rx.hstack(
                        rx.icon(
                            tag="lock",
                            size=24,
                            color=theme.Color.BLUE_300,  # Color azul del sistema
                        ),
                        rx.heading(
                            "Acceso Administrador",
                            size="6",
                            color=theme.Color.GRAY_900,  # Texto oscuro para contraste
                            font_family=theme.Typography.FONT_FAMILY,
                            font_weight=theme.Typography.FONT_WEIGHTS["semibold"],
                        ),
                        align_items="center",
                        spacing="3",
                        width="100%",
                    ),
                    
                    rx.text(
                        "Ingresa tus credenciales para continuar.",
                        color=theme.Color.GRAY_700,  # Texto secundario
                        font_family=theme.Typography.FONT_FAMILY,
                        text_align="center",
                        margin_bottom="1em",
                    ),
                    
                    # === FORMULARIO ===
                    rx.vstack(
                        # Campo email con estilo centralizado
                        rx.vstack(
                            rx.text(
                                "Correo electrónico",
                                color=theme.Color.GRAY_900,
                                font_family=theme.Typography.FONT_FAMILY,
                                font_weight=theme.Typography.FONT_WEIGHTS["medium"],
                                font_size="2",
                            ),
                            rx.input(
                                placeholder="admin@institucion.edu",
                                value=State.login_correo,
                                on_change=State.set_login_correo,
                                type="email",
                                width="100%",
                                # Usar estilos centralizados del tema
                                border=f"1px solid {theme.Color.GRAY_500}",
                                border_radius="6px",
                                padding="8px 12px",
                                font_family=theme.Typography.FONT_FAMILY,
                                bg=theme.Color.WHITE,
                                color="#000000",  # Negro explícito para el texto
                                _placeholder={"color": "#666666"},  # Gris para placeholder
                                _focus={
                                    "border_color": theme.Color.BLUE_300,
                                    "outline": "none",
                                    "box_shadow": f"0 0 0 2px {theme.Color.BLUE_300}40",
                                },
                            ),
                            align_items="start",
                            width="100%",
                            spacing="1",
                        ),
                        
                        # Campo contraseña con estilo centralizado
                        rx.vstack(
                            rx.text(
                                "Contraseña",
                                color=theme.Color.GRAY_900,
                                font_family=theme.Typography.FONT_FAMILY,
                                font_weight=theme.Typography.FONT_WEIGHTS["medium"],
                                font_size="2",
                            ),
                            rx.input(
                                placeholder="Tu contraseña",
                                value=State.login_password,
                                on_change=State.set_login_password,
                                type="password",
                                width="100%",
                                # Usar estilos centralizados del tema
                                border=f"1px solid {theme.Color.GRAY_500}",
                                border_radius="6px",
                                padding="8px 12px",
                                font_family=theme.Typography.FONT_FAMILY,
                                bg=theme.Color.WHITE,
                                color="#000000",  # Negro explícito para el texto
                                _placeholder={"color": "#666666"},  # Gris para placeholder
                                _focus={
                                    "border_color": theme.Color.BLUE_300,
                                    "outline": "none",
                                    "box_shadow": f"0 0 0 2px {theme.Color.BLUE_300}40",
                                },
                            ),
                            align_items="start",
                            width="100%",
                            spacing="1",
                        ),
                        
                        # === MENSAJE DE ERROR ===
                        rx.cond(
                            State.login_error != "",
                            rx.box(
                                rx.hstack(
                                    rx.icon(tag="triangle_alert", size=16, color="#dc2626"),
                                    rx.text(
                                        State.login_error,
                                        color="#dc2626",
                                        font_family=theme.Typography.FONT_FAMILY,
                                        font_size="2",
                                    ),
                                    spacing="2",
                                ),
                                padding="0.75em",
                                bg="#fef2f2",  # Fondo rojo claro para errores
                                border="1px solid #fecaca",
                                border_radius="6px",
                                width="100%",
                            ),
                        ),
                        
                        # === BOTONES DE ACCIÓN ===
                        rx.hstack(
                            rx.button(
                                "Cancelar",
                                on_click=State.toggle_login_dialog,
                                # Botón secundario con colores del tema
                                bg=theme.Color.GRAY_300,
                                color=theme.Color.GRAY_900,
                                border=f"1px solid {theme.Color.GRAY_500}",
                                font_family=theme.Typography.FONT_FAMILY,
                                font_weight=theme.Typography.FONT_WEIGHTS["medium"],
                                padding="8px 16px",
                                border_radius="6px",
                                cursor="pointer",
                                _hover={
                                    "bg": theme.Color.GRAY_500,
                                    "transform": "translateY(-1px)",
                                },
                                transition="all 0.2s ease-in-out",
                            ),
                            rx.button(
                                "Ingresar",
                                on_click=State.handle_login,
                                # Botón primario con colores del tema
                                bg=theme.Color.BLUE_300,
                                color="white",
                                font_family=theme.Typography.FONT_FAMILY,
                                font_weight=theme.Typography.FONT_WEIGHTS["medium"],
                                padding="8px 16px",
                                border_radius="6px",
                                cursor="pointer",
                                _hover={
                                    "bg": "#1565c0",  # Azul más oscuro al hover
                                    "transform": "translateY(-1px)",
                                },
                                transition="all 0.2s ease-in-out",
                            ),
                            spacing="3",
                            justify="end",
                            width="100%",
                        ),
                        
                        spacing="4",
                        width="100%",
                    ),
                    
                    spacing="4",
                    width="100%",
                ),
                # === ESTILOS DEL MODAL ===
                bg=theme.Color.DARK_CARD,  # Fondo oscuro consistente con el tema
                border=f"1px solid {theme.Color.GRAY_500}",
                border_radius="12px",
                padding="24px",
                max_width="400px",
                width="90%",
                box_shadow="0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)",
            ),
            # === OVERLAY DEL MODAL ===
            position="fixed",
            top="0",
            left="0",
            width="100vw",
            height="100vh",
            bg="rgba(0,0,0,0.6)",  # Overlay más oscuro para mejor contraste
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
