import reflex as rx
import os
from dotenv import load_dotenv
import saltoestudia.theme as theme
from saltoestudia.database import engine  # Importar el engine

# Carga las variables desde el archivo .env
load_dotenv()

# Configuración de la aplicación completa
config = rx.Config(
    app_name="saltoestudia",
    db_url=str(engine.url),  # Usar la URL del engine importado
    api_url="http://localhost:8000",
    frontend_port=3000,  # Forzar puerto 3000 explícitamente
    backend_port=8000,   # Forzar puerto 8000 explícitamente
    style=theme.STYLESHEET,
    head_components=[
        rx.script(src="/chakra_color_mode_provider.js"),
    ],
    # Configuración de Tailwind - Deshabilitado porque no lo usamos
    tailwind=None,
)
