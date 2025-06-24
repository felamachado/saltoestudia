# saltoestudia/constants.py

class CursosConstants:
    """Constantes para la gestión de cursos."""
    
    NIVELES = [
        "Bachillerato",
        "Terciario", 
        "Universitario",
        "Posgrado"
    ]
    
    DURACIONES_NUMEROS = [str(i) for i in range(1, 13)]  # 1 a 12
    
    DURACIONES_UNIDADES = [
        "meses",
        "años"
    ]
    
    REQUISITOS_INGRESO = [
        "Ciclo básico",
        "Bachillerato", 
        "Terciario",
        "Universitario"
    ]

class ValidationConstants:
    """Constantes para validación."""
    
    MAX_NOMBRE_CURSO = 200
    MAX_INFORMACION = 1000
    
    @classmethod
    def validate_nivel(cls, nivel: str) -> bool:
        return nivel in CursosConstants.NIVELES
    
    @classmethod 
    def validate_duracion_numero(cls, duracion: str) -> bool:
        return duracion in CursosConstants.DURACIONES_NUMEROS
    
    @classmethod
    def validate_duracion_unidad(cls, unidad: str) -> bool:
        return unidad in CursosConstants.DURACIONES_UNIDADES
    
    @classmethod
    def validate_requisitos(cls, requisito: str) -> bool:
        return requisito in CursosConstants.REQUISITOS_INGRESO 