import reflex as rx
from .database import obtener_instituciones, obtener_instituciones_nombres, obtener_cursos, obtener_niveles, obtener_requisitos
from typing import List, Dict, Any

class State(rx.State):
    cursos: List[Dict[str, Any]] = []
    niveles: List[str] = []
    requisitos: List[str] = []
    instituciones_nombres : List[str] = []
    nivel_seleccionado: str = ""
    duracion_seleccionada: str = ""
    requisito_seleccionado: str = ""
    institucion_seleccionada: str = ""
    instituciones_info: List[Dict[str, Any]] = []

    def cargar_niveles(self):
        """Load levels from the database."""
        niveles = obtener_niveles()
        self.niveles = ["Todos"] + niveles

    def cargar_requisitos(self):
        """Load requisitos from the database."""
        requisitos = obtener_requisitos()
        self.requisitos = ["Todos"] + requisitos

    def cargar_cursos(self):
        """Load courses from the database."""
        self.cursos = obtener_cursos()

    def cargar_instituciones_nombres(self):
        """Load institutions names from the database."""
        instituciones_nombres = obtener_instituciones_nombres()
        self.instituciones_nombres = ["Todos"] + instituciones_nombres

    def cargar_instituciones(self):
        """Load institutions from the database."""
        self.instituciones_info = obtener_instituciones()

    def actualizar_nivel_seleccionado(self, nivel: str):
        if nivel == "Todos":
            self.nivel_seleccionado = None
        else:
            self.nivel_seleccionado = nivel

    def actualizar_requisito_seleccionado(self, requisito: str):
        if requisito == "Todos":
            self.requisito_seleccionado = None
        else:
            self.requisito_seleccionado = requisito

    def actualizar_duracion_seleccionada(self, duracion: str):
        if duracion == "Todos":
            self.duracion_seleccionada = None
        else:
            self.duracion_seleccionada = int(duracion)

    def actualizar_institución_seleccionada(self, institucion: str):
        if institucion == "Todos":
            self.institucion_seleccionada = None
        else:
            self.institucion_seleccionada = institucion


    @rx.var
    def tabla_cursos(self) -> List[List[Any]]:
        """Compute the data for the table based on filters."""
        cursos_filtrados = [
            curso for curso in self.cursos
            if (not self.nivel_seleccionado or curso['nivel'] == self.nivel_seleccionado)
            and (not self.duracion_seleccionada or curso['duracion'] == self.duracion_seleccionada)
            and (not self.requisito_seleccionado or curso['requisitos_ingreso'] == self.requisito_seleccionado)
            and (not self.institucion_seleccionada or curso['institucion'] == self.institucion_seleccionada)
        ]
        return [
            [
                curso['nombre'],
                curso['nivel'],
                #curso['duracion'],
                f"{curso['duracion']} años",  # Concatenar duración con "años"
                curso['requisitos_ingreso'],
                curso['institucion'],  # Agregamos el campo de institución
                curso['informacion']
            ]
            for curso in cursos_filtrados
        ]