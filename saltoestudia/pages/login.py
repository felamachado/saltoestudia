# saltoestudia/pages/login.py

import reflex as rx
from ..layout import page_layout
from ..state import State
from .. import theme
from ..theme import ButtonStyle, ComponentStyle

@rx.page(route="/login", title="Iniciar Sesión | Salto Estudia")
def login_page() -> rx.Component:
    """Página dedicada de login para administradores."""
    return page_layout(
        rx.vstack(
            rx.box(
                rx.vstack(
                    # Logo o ícono
                    rx.icon(
                        tag="lock",
                        size=48,
                        color=theme.Color.BLUE_300,
                        margin_bottom="1em",
                    ),
                    
                    # Título
                    rx.heading(
                        "Acceso Administrativo",
                        size="8",
                        color=theme.Color.GRAY_900,
                        font_family=theme.Typography.FONT_FAMILY,
                        font_weight=theme.Typography.FONT_WEIGHTS["bold"],
                        text_align="center",
                        margin_bottom="0.5em",
                    ),
                    
                    # Subtítulo
                    rx.text(
                        "Inicia sesión para acceder al panel de administración",
                        color=theme.Color.GRAY_700,
                        font_family=theme.Typography.FONT_FAMILY,
                        text_align="center",
                        margin_bottom="2em",
                    ),
                    
                    # Formulario de login
                    rx.vstack(
                        # Campo email
                        rx.vstack(
                            rx.text(
                                "Correo electrónico",
                                **ComponentStyle.FORM_LABEL,
                                font_family=theme.Typography.FONT_FAMILY,
                            ),
                            rx.input(
                                placeholder="admin@institucion.edu",
                                type="email",
                                value=State.login_correo,
                                on_change=State.set_login_correo,
                                width="100%",
                                **ComponentStyle.FORM_INPUT,
                                font_family=theme.Typography.FONT_FAMILY,
                            ),
                            align_items="start",
                            width="100%",
                            spacing="1",
                        ),
                        
                        # Campo password
                        rx.vstack(
                            rx.text(
                                "Contraseña",
                                **ComponentStyle.FORM_LABEL,
                                font_family=theme.Typography.FONT_FAMILY,
                            ),
                            rx.input(
                                placeholder="Ingresa tu contraseña",
                                type="password",
                                value=State.login_password,
                                on_change=State.set_login_password,
                                width="100%",
                                **ComponentStyle.FORM_INPUT,
                                font_family=theme.Typography.FONT_FAMILY,
                            ),
                            align_items="start",
                            width="100%",
                            spacing="1",
                        ),
                        
                        # Mensaje de error
                        rx.cond(
                            State.login_error != "",
                            rx.box(
                                rx.hstack(
                                    rx.icon(tag="alarm_clock", size=16, color="#dc2626"),
                                    rx.text(State.login_error, color="#dc2626"),
                                    spacing="2",
                                ),
                                padding="0.75em",
                                bg="#fef2f2",
                                border="1px solid #fecaca",
                                border_radius="0.375em",
                                margin_top="1em",
                            ),
                        ),
                        
                        # Botón de login
                        rx.button(
                            "Iniciar Sesión",
                            on_click=State.handle_login_redirect,
                            width="100%",
                            **ButtonStyle.primary(),
                            font_family=theme.Typography.FONT_FAMILY,
                            font_weight=theme.Typography.FONT_WEIGHTS["medium"],
                            margin_top="1.5em",
                        ),
                        
                        spacing="4",
                        width="100%",
                    ),
                    
                    # Link para volver
                    rx.text(
                        "¿No eres administrador? ",
                        rx.link(
                            "Volver al inicio",
                            href="/",
                            color=theme.Color.BLUE_300,
                            _hover={"text_decoration": "underline"},
                        ),
                        color=theme.Color.GRAY_700,
                        font_family=theme.Typography.FONT_FAMILY,
                        text_align="center",
                        margin_top="2em",
                        font_size="2",
                    ),
                    
                    spacing="4",
                    align_items="center",
                    padding="3em",
                    width="100%",
                ),
                bg=theme.Color.DARK_CARD,
                border=f"1px solid {theme.Color.GRAY_500}",
                border_radius="12px",
                max_width="400px",
                width="90%",
                box_shadow="lg",
            ),
            min_height="70vh",
            width="100%",
            justify_content="center",
            align_items="center",
            padding="2em",
        )
    ) 