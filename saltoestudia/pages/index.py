# saltoestudia/pages/index.py

import reflex as rx
from ..layout import page_layout
from .. import theme

# === EFECTOS ÚNICOS DE REFLEX ===

def inject_magical_css():
    """Inyecta CSS personalizado para efectos mágicos - exclusivo de Reflex"""
    return rx.script(
        """
        // Verificar si ya existe el estilo para evitar duplicados
        if (!document.getElementById('magical-styles')) {
            const style = document.createElement('style');
            style.id = 'magical-styles';
            style.textContent = `
                @keyframes iconFloat {
                    0%, 100% { transform: translateY(0px) rotate(0deg); }
                    25% { transform: translateY(-6px) rotate(1deg); }
                    50% { transform: translateY(-3px) rotate(0deg); }
                    75% { transform: translateY(-9px) rotate(-1deg); }
                }
                
                @keyframes iconFloatMobile {
                    0%, 100% { transform: translateY(0px) rotate(0deg); }
                    25% { transform: translateY(-4px) rotate(0.5deg); }
                    50% { transform: translateY(-2px) rotate(0deg); }
                    75% { transform: translateY(-6px) rotate(-0.5deg); }
                }
                
                .magic-card:hover .icon-hover-target {
                    animation: iconFloat 2s ease-in-out infinite !important;
                }
                
                .magic-card-mobile:hover .icon-hover-target-mobile {
                    animation: iconFloatMobile 2.5s ease-in-out infinite !important;
                }
                
                [data-card-type="desktop"]:hover [data-icon-float] {
                    animation: iconFloat 2s ease-in-out infinite !important;
                }
                
                [data-card-type="mobile"]:hover [data-icon-float] {
                    animation: iconFloatMobile 2.5s ease-in-out infinite !important;
                }
            `;
            document.head.appendChild(style);
        }
        """
    )

# --- DECORADOR AÑADIDO ---
# Esta línea es la que registra la función como la página de inicio.
@rx.page(route="/", title="Inicio | Salto Estudia")
def index() -> rx.Component:
    return page_layout(
        # === EFECTOS MÁGICOS ÚNICOS DE REFLEX ===
        inject_magical_css(),
        
        # === VERSIÓN DESKTOP ===
        rx.desktop_only(
            rx.box(
                # Contenido principal
                rx.vstack(
                    rx.heading("¡Bienvenidos!", size="9", color=theme.Color.BLUE_300),
                    rx.text(
                        "En Salto Estudia vas a poder encontrar la oferta educativa local que mejor se adapta a vos.",
                        size="4",
                        color=theme.Color.GRAY_900,
                        text_align="center",
                        max_width="600px",
                    ),
                    rx.hstack(
                        tarjeta_desktop("Instituciones", "Conocé las instituciones educativas.", "info", "/instituciones"),
                        tarjeta_desktop("Cursos", "Explorá todos los cursos disponibles.", "search", "/cursos"),
                        spacing="6",
                    ),
                    align_items="center",
                    justify="center",
                    spacing="6",
                    padding="20px",
                    height="calc(100vh - 56px)",  # Altura disponible sin header
                    width="100%",
                ),
                position="fixed",  # Posición fija para ocupar toda la pantalla
                top="56px",  # Debajo del header
                left="0",
                right="0",
                bottom="0",
                overflow="hidden",
                display="flex",
                align_items="center",
                justify_content="center",
            )
        ),
        
        # === VERSIÓN MÓVIL Y TABLET ===
        rx.mobile_and_tablet(
            rx.vstack(
                rx.heading(
                    "¡Bienvenidos!", 
                    size="7", 
                    color=theme.Color.BLUE_300,
                    text_align="center",
                ),
                rx.text(
                    "En Salto Estudia vas a poder encontrar la oferta educativa local que mejor se adapta a vos.",
                    size="3",
                    color=theme.Color.GRAY_900,
                    text_align="center",
                    line_height="1.6",
                ),
                rx.vstack(
                    tarjeta_mobile("Instituciones", "Conocé las instituciones educativas.", "info", "/instituciones"),
                    tarjeta_mobile("Cursos", "Explorá todos los cursos disponibles.", "search", "/cursos"),
                    spacing="4",
                    width="100%",
                ),
                align_items="center",
                padding="20px",
                spacing="6",
                width="100%",
                height="calc(100vh - 56px)",  # Altura disponible sin header
                justify="center",
                position="fixed",
                top="56px",
                left="0",
                right="0",
                bottom="0",
                overflow="hidden",
            )
        ),
    )

def tarjeta_desktop(titulo, descripcion, icono, link=None):
    """Tarjeta con efectos de luces y ícono flotante solo en hover"""
    return rx.box(
        rx.vstack(
            # Ícono que solo se mueve en hover de la tarjeta
            rx.box(
                rx.icon(tag=icono, size=50, color=theme.Color.BLUE_300),
                # Sin animación inicial, solo en hover del padre
                class_name="icon-hover-target",
                # Alternativa con data attribute
                data_icon_float="true",
            ),
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
            justify="between",
            spacing="3",
            height="100%",
        ),
        padding="32px",
        shadow="lg",
        border_radius="12px",
        cursor="pointer",
        on_click=(rx.redirect(link) if link else None),
        bg=theme.Color.DARK_CARD,
        border=f"1px solid {theme.Color.GRAY_500}",
        width="300px",
        height="280px",
        # Adaptarse al viewport disponible
        max_width="45vw",  # Máximo 45% del ancho de viewport
        min_width="250px",  # Mínimo para mantener legibilidad
        # === TARJETA ESTÁTICA CON LUCES EN HOVER ===
        # Sin animación continua de la tarjeta
        background="linear-gradient(45deg, #1f2937, #374151)",
        transition="all 0.5s ease",
        class_name="magic-card",
        # Alternativa con data attribute
        data_card_type="desktop",
                 _hover={
             # Efecto neon más suave (luces menos potentes)
             "box_shadow": "0 0 8px rgba(59, 130, 246, 0.4), 0 0 16px rgba(59, 130, 246, 0.3), 0 0 24px rgba(59, 130, 246, 0.2), 0 0 32px rgba(59, 130, 246, 0.1)",
             "border_color": theme.Color.BLUE_300,
             "border_width": "2px",
             # Gradiente más vibrante en hover
             "background": "linear-gradient(45deg, #374151, #4b5563)",
         }
    )

def tarjeta_mobile(titulo, descripcion, icono, link=None):
    """Tarjeta móvil con luces suaves y ícono flotante solo en hover"""
    return rx.box(
        rx.vstack(
            # Ícono que solo se mueve en hover para móvil
            rx.box(
                rx.icon(tag=icono, size=40, color=theme.Color.BLUE_300),
                # Sin animación inicial, solo en hover del padre
                class_name="icon-hover-target-mobile",
                # Alternativa con data attribute
                data_icon_float="true",
            ),
            rx.text(
                titulo, 
                font_weight="bold", 
                size="5", 
                color=theme.Color.GRAY_900,
                text_align="center"
            ),
            rx.text(
                descripcion, 
                text_align="center", 
                color=theme.Color.GRAY_700,
                size="3",
                line_height="1.4"
            ),
            align_items="center",
            justify="center",
            spacing="3",
            height="100%",
        ),
        padding="24px",
        shadow="lg",
        border_radius="12px",
        cursor="pointer",
        on_click=(rx.redirect(link) if link else None),
        bg=theme.Color.DARK_CARD,
        border=f"1px solid {theme.Color.GRAY_500}",
        width="100%",
        min_height="180px",
        # Adaptación responsive para móvil
        height="25vh",  # 25% de la altura del viewport
        max_height="220px",
        # === TARJETA MÓVIL ESTÁTICA CON LUCES ===
        # Sin animación continua de la tarjeta
        background="linear-gradient(45deg, #1f2937, #374151)",
        transition="all 0.4s ease",
        class_name="magic-card-mobile",
        # Alternativa con data attribute
        data_card_type="mobile",
                 _hover={
             # Efecto neon aún más suave para móvil
             "box_shadow": "0 0 6px rgba(59, 130, 246, 0.3), 0 0 12px rgba(59, 130, 246, 0.2), 0 0 18px rgba(59, 130, 246, 0.1)",
             "border_color": theme.Color.BLUE_300,
             "background": "linear-gradient(45deg, #374151, #4b5563)",
         }
    )
