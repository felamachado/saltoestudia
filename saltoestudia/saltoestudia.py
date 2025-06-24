# saltoestudia.py

import reflex as rx
# Importar páginas principales
from .pages.index import index
from .pages.instituciones import instituciones
from .pages.cursos import cursos
from .pages.info import info
from .pages.admin import admin_page
from .pages.login import login_page
from . import models

# Configuración original con Bootstrap CSS
app = rx.App(
    stylesheets=["https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css"]
)

# NO es necesario llamar a app.add_page() para las páginas que usan el decorador @rx.page.
# El decorador ya las registra automáticamente. Al llamar a add_page de nuevo,
# se genera la advertencia "redefined with the same component".
# Simplemente con importar las páginas arriba es suficiente.
