import reflex as rx

from .pages.index import index
from .pages.instituciones import instituciones
from .pages.cursos import cursos
from .pages.info import info

# Definir las rutas de la aplicación
app = rx.App(
    stylesheets=["https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css"]
)

app.add_page(index, route="/")
app.add_page(instituciones, route="/instituciones")
app.add_page(cursos, route="/cursos")
app.add_page(info, route="/info")
