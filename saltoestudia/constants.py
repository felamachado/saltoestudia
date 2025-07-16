# ================================================================================
# CONSTANTES DEL SISTEMA - SALTO ESTUDIA
# ================================================================================
# 
# Este archivo centraliza todas las constantes utilizadas en el sistema,
# especialmente para la gestión de cursos y validaciones de datos.
#
# PROPÓSITO:
# - Evitar valores hardcodeados dispersos en el código
# - Facilitar mantenimiento y cambios de valores
# - Proporcionar validaciones centralizadas
# - Asegurar consistencia en toda la aplicación
#
# UTILIZADO EN:
# - state.py: Para poblar dropdowns y opciones de filtros
# - database.py: Para validar datos antes de persistir
# - pages/cursos.py: Para filtros del buscador público
# - pages/admin.py: Para formularios de administración
# ================================================================================

class CursosConstants:
    """
    Constantes para la gestión de cursos educativos.
    
    Define los valores permitidos para los campos de cursos, asegurando
    consistencia en toda la aplicación y facilitando el mantenimiento.
    
    CAMPOS DEFINIDOS:
    - NIVELES: Niveles educativos disponibles en Uruguay
    - DURACIONES_NUMEROS: Rangos numéricos para duración de cursos
    - DURACIONES_UNIDADES: Unidades de tiempo válidas
    - REQUISITOS_INGRESO: Requisitos educativos previos
    - LUGARES: Lugares donde se pueden dictar cursos (ciudades + virtual)
    
    PATRÓN DE USO:
    Estas constantes se utilizan para:
    1. Poblar dropdowns en formularios
    2. Validar datos de entrada
    3. Filtrar información en búsquedas
    4. Mantener consistencia en la UI
    """
    
    # === NIVELES EDUCATIVOS ===
    # Niveles del sistema educativo uruguayo, desde secundaria hasta posgrado
    NIVELES = [
        "Bachillerato",   # Educación secundaria completa (6to año)
        "Terciario",      # Educación superior no universitaria
        "Universitario",  # Grado universitario (licenciaturas, ingenierías)
        "Posgrado"        # Especialización, maestrías, doctorados
    ]
    
    # === DURACIONES NUMÉRICAS ===
    # Rango de 1 a 12 para cubrir desde cursos cortos hasta carreras largas
    # Se convierte a strings para compatibilidad con formularios web
    DURACIONES_NUMEROS = [str(i) for i in range(1, 13)]  # ["1", "2", ..., "12"]
    
    # === UNIDADES DE TIEMPO ===
    # Unidades más comunes para duración de cursos educativos
    DURACIONES_UNIDADES = [
        "meses",  # Para cursos cortos, talleres, capacitaciones
        "años"    # Para carreras largas, licenciaturas, ingenierías
    ]
    
    # === REQUISITOS DE INGRESO ===
    # Requisitos educativos previos necesarios para acceder a cada nivel
    REQUISITOS_INGRESO = [
        "Ciclo básico",   # Primeros 3 años de secundaria (1ro-3ro)
        "Bachillerato",   # Secundaria completa (hasta 6to)
        "Terciario",      # Título terciario previo
        "Universitario"   # Título universitario previo
    ]

    # Lista de lugares donde se pueden dictar cursos (ciudades + virtual)
    LUGARES = [
        "Virtual",              # Modalidad online/remota
        "Artigas",              # Capital del departamento de Artigas
        "Salto",                # Capital del departamento de Salto
        "Paysandú",             # Capital del departamento de Paysandú
        "Mercedes",             # Capital del departamento de Soriano
        "Fray Bentos",          # Capital del departamento de Río Negro
        "Colonia del Sacramento", # Capital del departamento de Colonia
        "San José de Mayo",     # Capital del departamento de San José
        "Montevideo",           # Capital del departamento de Montevideo
        "Canelones",            # Capital del departamento de Canelones
        "Florida",              # Capital del departamento de Florida
        "Minas",                # Capital del departamento de Lavalleja
        "Rocha",                # Capital del departamento de Rocha
        "Treinta y Tres",       # Capital del departamento de Treinta y Tres
        "Melo",                 # Capital del departamento de Cerro Largo
        "Rivera",               # Capital del departamento de Rivera
        "Tacuarembó",           # Capital del departamento de Tacuarembó
        "Durazno",              # Capital del departamento de Durazno
        "Trinidad"              # Capital del departamento de Flores
    ]

class ValidationConstants:
    """
    Constantes para validación de datos en el sistema.
    
    Proporciona límites y métodos de validación para asegurar
    la integridad de los datos ingresados por los usuarios.
    
    LÍMITES DEFINIDOS:
    - Longitud máxima de campos de texto
    - Validadores para cada tipo de campo
    
    MÉTODOS DE VALIDACIÓN:
    - validate_nivel(): Valida niveles educativos
    - validate_duracion_numero(): Valida duración numérica
    - validate_duracion_unidad(): Valida unidades de tiempo
    - validate_requisitos(): Valida requisitos de ingreso
    
    UTILIZADO EN:
    - database.py: Validación antes de operaciones CRUD
    - Formularios: Validación del lado del cliente
    - APIs: Validación de datos de entrada
    """
    
    # === LÍMITES DE LONGITUD ===
    # Límites para campos de texto libre en la base de datos
    MAX_NOMBRE_CURSO = 200      # Límite para el nombre del curso
    MAX_INFORMACION = 1000      # Límite para información adicional
    
    # === MÉTODOS DE VALIDACIÓN ===
    # Cada método valida que el valor esté dentro de las opciones permitidas
    
    @classmethod
    def validate_nivel(cls, nivel: str) -> bool:
        """
        Valida que el nivel educativo sea uno de los permitidos.
        
        Args:
            nivel: Nivel educativo a validar
            
        Returns:
            bool: True si es válido, False en caso contrario
            
        Utilizado en:
        - database.py: agregar_curso() y modificar_curso()
        - Formularios de administración antes del envío
        """
        return nivel in CursosConstants.NIVELES
    
    @classmethod 
    def validate_duracion_numero(cls, duracion: str) -> bool:
        """
        Valida que la duración numérica esté en el rango permitido.
        
        Args:
            duracion: Duración numérica como string
            
        Returns:
            bool: True si está en rango 1-12, False en caso contrario
        """
        return duracion in CursosConstants.DURACIONES_NUMEROS
    
    @classmethod
    def validate_duracion_unidad(cls, unidad: str) -> bool:
        """
        Valida que la unidad de tiempo sea una de las permitidas.
        
        Args:
            unidad: Unidad de tiempo a validar
            
        Returns:
            bool: True si es "meses" o "años", False en caso contrario
        """
        return unidad in CursosConstants.DURACIONES_UNIDADES
    
    @classmethod
    def validate_requisitos(cls, requisito: str) -> bool:
        """
        Valida que el requisito de ingreso sea uno de los permitidos.
        
        Args:
            requisito: Requisito educativo a validar
            
        Returns:
            bool: True si es válido, False en caso contrario
        """
        return requisito in CursosConstants.REQUISITOS_INGRESO
    
    @classmethod
    def validate_lugar(cls, lugar: str) -> bool:
        """
        Valida que el lugar sea uno de los permitidos.
        
        Args:
            lugar: Lugar donde se dicta el curso (ciudad o virtual)
            
        Returns:
            bool: True si es válido, False en caso contrario
        """
        return lugar in CursosConstants.LUGARES

# ================================================================================
# NOTAS DE IMPLEMENTACIÓN
# ================================================================================
#
# EXTENSIBILIDAD:
# Para agregar nuevos valores, simplemente añadir a las listas correspondientes.
# El sistema automáticamente los reflejará en:
# - Dropdowns de formularios
# - Opciones de filtrado
# - Validaciones de datos
#
# MANTENIMIENTO:
# - Cambios aquí se propagan automáticamente a toda la aplicación
# - No requiere modificar múltiples archivos
# - Facilita auditorías y cambios de requisitos
#
# LOCALIZACIÓN:
# - Los valores están en español para usuarios uruguayos
# - Fácil traducir cambiando solo este archivo
# - Mantiene consistencia terminológica 