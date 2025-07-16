# 🧩 Componentes del Sistema - Salto Estudia

## 📋 Resumen

Este documento describe en detalle todos los componentes del sistema Salto Estudia, desde los módulos principales hasta las funciones específicas.

## 🏗️ Módulos Principales

### 1. `saltoestudia.py` - Punto de Entrada

**Propósito**: Configuración global de la aplicación Reflex y registro de páginas.

**Funcionalidades**:
- Configuración de la aplicación con Bootstrap CSS
- Importación automática de todas las páginas
- Registro de modelos SQLModel

**Código Clave**:
```python
app = rx.App(
    stylesheets=[
        "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css"
    ]
)
```

---

### 2. `state.py` - Gestión de Estado Global

**Propósito**: Núcleo del sistema de gestión de estado reactivo.

#### Clase `User`
```python
class User(rx.Base):
    """
    Modelo de usuario seguro para el estado de Reflex.
    Excluye información sensible como contraseñas.
    """
    id: int                      # ID único del usuario
    correo: str                  # Email para mostrar en UI
    institucion_id: int          # ID de institución para filtros CRUD
    institucion_nombre: str      # Nombre para mostrar en header admin
```

#### Clase `State` - Organización por Funcionalidades

##### Cursos Públicos
```python
# Datos de cursos
cursos: List[Dict[str, Any]] = []                    # Cursos filtrados mostrados en UI
cursos_originales: List[Dict[str, Any]] = []         # Todos los cursos sin filtrar (cache)

# Cache y performance
cursos_cache_loaded: bool = False                    # Flag de cache de cursos cargado
instituciones_cache_loaded: bool = False             # Flag de cache de instituciones cargado
ciudades_cache_loaded: bool = False                  # Flag de cache de ciudades cargado

# Filtros de búsqueda
nivel_seleccionado: str = ""                         # Filtro por nivel educativo
duracion_seleccionada: str = ""                      # Filtro por duración
requisito_seleccionado: str = ""                     # Filtro por requisitos de ingreso
institucion_seleccionada: str = ""                   # Filtro por institución
lugar_seleccionado: str = ""                         # Filtro por lugar
busqueda_texto: str = ""                             # Filtro de búsqueda manual
```

##### Autenticación
```python
# Modal login
show_login_dialog: bool = False                      # Control modal login en header
login_correo: str = ""                               # Campo email del formulario
login_password: str = ""                             # Campo contraseña del formulario
login_error: str = ""                                # Mensaje de error de autenticación

# Sesión de usuario
logged_in_user: Optional[User] = None                # Usuario autenticado actual
user_authenticated: bool = False                     # Flag adicional de autenticación
redirect_url: str = ""                               # URL para redirigir post-login
```

##### Admin CRUD
```python
# Datos admin
admin_cursos: List[Dict[str, Any]] = []              # Cursos de la institución del admin
admin_sedes: List[Dict[str, Any]] = []               # Sedes de la institución del admin

# UI Control - Formulario cursos
show_curso_dialog: bool = False                      # Control modal formulario curso
is_editing: bool = False                             # Modo edición vs creación
curso_a_editar: Dict[str, Any] = {}                  # Datos del curso en edición

# Campos del formulario curso
form_nombre: str = ""                                # Campo nombre del curso
form_nivel: str = ""                                 # Campo nivel educativo
form_duracion_numero: str = ""                       # Campo duración numérica
form_duracion_unidad: str = ""                       # Campo unidad de tiempo
form_requisitos_ingreso: str = ""                    # Campo requisitos previos
form_lugar: str = ""                                 # Campo lugar donde se dicta el curso
form_informacion: str = ""                           # Campo información adicional
form_ciudades: List[str] = []                        # Lista de ciudades seleccionadas
```

#### Métodos Principales

##### Gestión de Cursos
```python
def cargar_cursos(self):
    """
    Carga todos los cursos desde la base de datos con cache inteligente.
    Evita recargas innecesarias usando flags de cache.
    """

def aplicar_filtros(self):
    """
    Aplica los filtros seleccionados a los cursos.
    Filtra por nivel, requisitos, institución, lugar y texto de búsqueda.
    """

def cargar_datos_cursos_page(self):
    """
    Carga los datos iniciales de la página de cursos con optimización de cold start.
    Implementa progressive loading para mejorar la experiencia de usuario.
    """
```

##### Autenticación
```python
def handle_login(self):
    """
    Maneja el proceso de autenticación del usuario.
    Valida credenciales con bcrypt y crea sesión de usuario.
    """

def handle_logout(self):
    """
    Cierra la sesión del usuario y limpia el estado.
    Redirige a la página de inicio.
    """
```

##### Gestión Admin
```python
def agregar_curso(self):
    """
    Agrega un nuevo curso a la base de datos.
    Valida datos antes de persistir.
    """

def modificar_curso(self):
    """
    Modifica un curso existente en la base de datos.
    Actualiza solo los campos modificados.
    """

def eliminar_curso(self):
    """
    Elimina un curso de la base de datos.
    Requiere confirmación del usuario.
    """
```

---

### 3. `database.py` - Operaciones de Base de Datos

**Propósito**: Capa de abstracción entre los modelos SQLModel y la UI.

#### Configuración del Engine
```python
# Engine único compartido entre la aplicación y scripts de seed
engine = create_engine(
    os.getenv("DATABASE_URL", "sqlite:///./data/saltoestudia.db"),
    echo=False  # Desactivar logs SQL en producción
)
```

#### Operaciones de Lectura

##### Cursos
```python
def obtener_cursos() -> List[Dict[str, Any]]:
    """
    Obtiene todos los cursos con información de institución.
    Optimizada para consultas públicas con joins eficientes.
    """

def obtener_cursos_por_institucion(institucion_id: int) -> List[Dict[str, Any]]:
    """
    Obtiene cursos filtrados por institución.
    Usado en el panel de administración.
    """
```

##### Instituciones
```python
def obtener_instituciones() -> List[Dict[str, Any]]:
    """
    Obtiene todas las instituciones con información completa.
    Incluye sedes y cursos para la galería.
    """

def obtener_instituciones_nombres() -> List[str]:
    """
    Obtiene solo los nombres de instituciones.
    Optimizada para poblar dropdowns de filtros.
    """
```

##### Usuarios
```python
def obtener_usuario_por_correo(correo: str) -> Optional[Usuario]:
    """
    Obtiene usuario por correo con eager loading de institución.
    Usado para autenticación con optimización de queries.
    """
```

#### Operaciones de Escritura

##### Cursos
```python
def agregar_curso(
    nombre: str,
    nivel: str,
    duracion_numero: str,
    duracion_unidad: str,
    requisitos_ingreso: str,
    lugar: str,
    informacion: str,
    institucion_id: int,
    ciudades: List[str] = None
) -> bool:
    """
    Agrega un nuevo curso con validaciones.
    Incluye soporte para múltiples ciudades.
    """

def modificar_curso(
    curso_id: int,
    nombre: str,
    nivel: str,
    duracion_numero: str,
    duracion_unidad: str,
    requisitos_ingreso: str,
    lugar: str,
    informacion: str,
    ciudades: List[str] = None
) -> bool:
    """
    Modifica un curso existente.
    Actualiza relaciones con ciudades si se especifican.
    """

def eliminar_curso(curso_id: int) -> bool:
    """
    Elimina un curso y sus relaciones.
    Limpia automáticamente las relaciones con ciudades.
    """
```

##### Sedes
```python
def agregar_sede(
    nombre: str,
    direccion: str,
    telefono: str,
    email: str,
    web: str,
    ciudad: str,
    institucion_id: int
) -> bool:
    """
    Agrega una nueva sede a una institución.
    Valida que la institución exista.
    """
```

#### Validaciones
```python
def validar_datos_curso(
    nombre: str,
    nivel: str,
    duracion_numero: str,
    duracion_unidad: str,
    requisitos_ingreso: str,
    lugar: str,
    informacion: str
) -> Tuple[bool, str]:
    """
    Valida todos los campos de un curso antes de persistir.
    Retorna (es_válido, mensaje_error).
    """
```

---

### 4. `models.py` - Modelos de Datos

**Propósito**: Define la estructura de datos y relaciones de la base de datos.

#### Modelo `Institucion`
```python
class Institucion(SQLModel, table=True):
    """
    Representa una institución educativa en Salto, Uruguay.
    Entidad central del sistema con múltiples relaciones.
    """
    __tablename__ = "instituciones"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str                           # Nombre oficial de la institución
    logo: Optional[str] = None            # Ruta al archivo de logo
    
    # Relaciones
    sedes: List["Sede"] = Relationship(back_populates="institucion")
    cursos: List["Curso"] = Relationship(back_populates="institucion")
    usuarios: List["Usuario"] = Relationship(back_populates="institucion")
```

#### Modelo `Curso`
```python
class Curso(SQLModel, table=True):
    """
    Representa un curso educativo ofrecido por una institución.
    Puede dictarse en múltiples ciudades.
    """
    __tablename__ = "cursos"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=200)
    nivel: str
    duracion_numero: str
    duracion_unidad: str
    requisitos_ingreso: str
    lugar: str
    informacion: Optional[str] = Field(max_length=1000, default=None)
    institucion_id: int = Field(foreign_key="instituciones.id")
    
    # Relaciones
    institucion: Optional[Institucion] = Relationship(back_populates="cursos")
    ciudades: List["Ciudad"] = Relationship(
        back_populates="cursos",
        link_model=CursoCiudadLink
    )
```

#### Modelo `Usuario`
```python
class Usuario(SQLModel, table=True):
    """
    Representa un usuario administrador del sistema.
    Pertenece a una institución específica.
    """
    __tablename__ = "usuarios"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    correo: str = Field(unique=True, index=True)
    password_hash: str
    institucion_id: int = Field(foreign_key="instituciones.id")
    
    # Relaciones
    institucion: Optional[Institucion] = Relationship(back_populates="usuarios")
```

#### Modelo `Sede`
```python
class Sede(SQLModel, table=True):
    """
    Representa una sede física de una institución.
    Contiene información de contacto y ubicación.
    """
    __tablename__ = "sedes"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    direccion: str
    telefono: str
    email: str
    web: str
    ciudad: str
    institucion_id: int = Field(foreign_key="instituciones.id")
    
    # Relaciones
    institucion: Optional[Institucion] = Relationship(back_populates="sedes")
```

#### Modelo `Ciudad`
```python
class Ciudad(SQLModel, table=True):
    """
    Representa una ciudad donde se pueden dictar cursos.
    Relación muchos a muchos con cursos.
    """
    __tablename__ = "ciudades"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(unique=True, index=True)
    
    # Relaciones
    cursos: List[Curso] = Relationship(
        back_populates="ciudades",
        link_model=CursoCiudadLink
    )
```

#### Tabla de Enlace `CursoCiudadLink`
```python
class CursoCiudadLink(SQLModel, table=True):
    """
    Tabla de enlace para relación muchos a muchos entre cursos y ciudades.
    """
    __tablename__ = "curso_ciudad_link"
    
    curso_id: Optional[int] = Field(
        default=None, 
        foreign_key="cursos.id", 
        primary_key=True
    )
    ciudad_id: Optional[int] = Field(
        default=None, 
        foreign_key="ciudades.id", 
        primary_key=True
    )
```

---

### 5. `constants.py` - Constantes del Sistema

**Propósito**: Centraliza todas las constantes utilizadas en el sistema.

#### Clase `CursosConstants`
```python
class CursosConstants:
    """
    Constantes para la gestión de cursos educativos.
    Define valores permitidos para campos de cursos.
    """
    
    # Niveles educativos del sistema uruguayo
    NIVELES = [
        "Bachillerato",   # Educación secundaria completa
        "Terciario",      # Educación superior no universitaria
        "Universitario",  # Grado universitario
        "Posgrado"        # Especialización, maestrías, doctorados
    ]
    
    # Duración numérica (1-12)
    DURACIONES_NUMEROS = [str(i) for i in range(1, 13)]
    
    # Unidades de tiempo
    DURACIONES_UNIDADES = [
        "meses",  # Para cursos cortos
        "años"    # Para carreras largas
    ]
    
    # Requisitos educativos previos
    REQUISITOS_INGRESO = [
        "Ciclo básico",   # Primeros 3 años de secundaria
        "Bachillerato",   # Secundaria completa
        "Terciario",      # Título terciario previo
        "Universitario"   # Título universitario previo
    ]
    
    # Lugares donde se pueden dictar cursos
    LUGARES = [
        "Virtual",              # Modalidad online
        "Artigas", "Salto", "Paysandú", "Mercedes", "Fray Bentos",
        "Colonia del Sacramento", "San José de Mayo", "Montevideo",
        "Canelones", "Florida", "Minas", "Rocha", "Treinta y Tres",
        "Melo", "Rivera", "Tacuarembó", "Durazno", "Trinidad"
    ]
```

#### Clase `ValidationConstants`
```python
class ValidationConstants:
    """
    Constantes para validación de datos en el sistema.
    Proporciona límites y métodos de validación.
    """
    
    # Límites de longitud
    MAX_NOMBRE_CURSO = 200      # Límite para nombre del curso
    MAX_INFORMACION = 1000      # Límite para información adicional
    
    # Métodos de validación
    @classmethod
    def validate_nivel(cls, nivel: str) -> bool:
        """Valida que el nivel educativo sea válido."""
        return nivel in CursosConstants.NIVELES
    
    @classmethod
    def validate_duracion_numero(cls, duracion: str) -> bool:
        """Valida que la duración numérica esté en rango 1-12."""
        return duracion in CursosConstants.DURACIONES_NUMEROS
    
    @classmethod
    def validate_duracion_unidad(cls, unidad: str) -> bool:
        """Valida que la unidad de tiempo sea válida."""
        return unidad in CursosConstants.DURACIONES_UNIDADES
    
    @classmethod
    def validate_requisitos(cls, requisito: str) -> bool:
        """Valida que el requisito de ingreso sea válido."""
        return requisito in CursosConstants.REQUISITOS_INGRESO
    
    @classmethod
    def validate_lugar(cls, lugar: str) -> bool:
        """Valida que el lugar sea válido."""
        return lugar in CursosConstants.LUGARES
```

---

### 6. `theme.py` - Sistema de Diseño

**Propósito**: Centraliza todos los estilos y componentes visuales del sistema.

#### Configuración de Tipografía
```python
class Typography:
    """Configuración de tipografía para toda la aplicación."""
    FONT_FAMILY = "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell', sans-serif"
    FONT_WEIGHTS = {
        "light": "300",
        "normal": "400", 
        "medium": "500",
        "semibold": "600",
        "bold": "700"
    }
```

#### Paleta de Colores
```python
class Color:
    """Paleta de colores para la aplicación."""
    # Escala de azules pastel
    BLUE_100 = "#E0F2FE"
    BLUE_300 = "#7DD3FC"
    BLUE_500 = "#0EA5E9"
    BLUE_700 = "#0369A1"
    
    # Escala de grises y negros
    GRAY_100 = "#1F2937"  # Fondo principal
    GRAY_300 = "#374151"  # Gris medio oscuro
    GRAY_500 = "#6B7280"  # Gris medio
    GRAY_700 = "#9CA3AF"  # Gris claro para texto
    GRAY_900 = "#F9FAFB"  # Texto principal
    
    # Colores semánticos
    PRIMARY = "#004A99"           # Azul principal del proyecto
    PRIMARY_HOVER = "#003875"     # Azul más oscuro para hover
    SUCCESS = "#10B981"           # Verde para éxito
    WARNING = "#F59E0B"           # Amarillo para advertencias
    DANGER = "#EF4444"            # Rojo para peligro/eliminar
```

#### Estilos de Botones
```python
class ButtonStyle:
    """Estilos de botones reutilizables."""
    
    @staticmethod
    def primary(**kwargs):
        """Botón principal del proyecto."""
        return {
            "bg": Color.PRIMARY,
            "color": Color.WHITE,
            "_hover": {"bg": Color.PRIMARY_HOVER},
            "border": "none",
            **kwargs
        }
    
    @staticmethod
    def secondary(**kwargs):
        """Botón secundario con outline."""
        return {
            "variant": "outline",
            "border_color": Color.PRIMARY,
            "color": Color.PRIMARY,
            "_hover": {
                "bg": Color.PRIMARY_LIGHT,
                "border_color": Color.PRIMARY_HOVER,
            },
            **kwargs
        }
    
    @staticmethod
    def danger(**kwargs):
        """Botón de peligro para acciones destructivas."""
        return {
            "bg": Color.DANGER,
            "color": Color.WHITE,
            "_hover": {"bg": Color.DANGER_HOVER},
            "border": "none",
            **kwargs
        }
```

#### Estilos de Componentes
```python
class ComponentStyle:
    """Estilos para componentes específicos."""
    
    # Estilos para tablas
    TABLE = {
        "variant": "surface",
        "width": "100%",
        "bg": Color.WHITE,
        "border": f"1px solid {Color.GRAY_500}",
        "border_radius": "8px",
        "size": "3",
    }
    
    TABLE_HEADER = {
        "color": Color.GRAY_900,
        "bg": Color.GRAY_300,
    }
    
    TABLE_CELL = {
        "color": Color.GRAY_900,
        "bg": Color.WHITE,
        "border_bottom": f"1px solid {Color.GRAY_500}",
        "padding": "12px",
    }
    
    # Estilos para formularios
    FORM_INPUT = {
        "bg": Color.GRAY_300,
        "color": Color.GRAY_900,
        "border_color": Color.GRAY_500,
        "_placeholder": {"color": Color.GRAY_900, "opacity": "0.6"},
        "_hover": {"border_color": Color.BLUE_300},
        "_focus": {
            "border_color": Color.BLUE_300, 
            "box_shadow": f"0 0 0 1px {Color.BLUE_300}"
        },
    }
    
    FORM_SELECT = {
        "bg": Color.GRAY_300,
        "color": Color.GRAY_900,
        "border_color": Color.GRAY_500,
        "_placeholder": {"color": Color.GRAY_900, "opacity": "0.6"},
        "_hover": {"border_color": Color.BLUE_300},
        "_focus": {
            "border_color": Color.BLUE_300, 
            "box_shadow": f"0 0 0 1px {Color.BLUE_300}"
        },
    }
```

#### Funciones de Utilidad
```python
def create_button(text: str, button_type: str = "primary", on_click=None, **kwargs):
    """
    Crea un botón con estilos predefinidos.
    
    Args:
        text: Texto del botón
        button_type: Tipo de botón (primary, secondary, danger, success)
        on_click: Función a ejecutar al hacer click
        **kwargs: Propiedades adicionales
    
    Returns:
        rx.button: Componente de botón con estilos aplicados
    """

def create_course_table_header(headers: list):
    """
    Crea el header de una tabla de cursos.
    
    Args:
        headers: Lista de títulos de columnas
    
    Returns:
        Lista de componentes rx.table.header_cell
    """

def create_custom_dropdown_css():
    """
    Inyecta CSS personalizado para solucionar problemas de estilos en dropdowns.
    Específicamente para el fondo blanco en opciones de dropdown.
    
    Returns:
        rx.script: Script con CSS personalizado
    """
```

---

### 7. `layout.py` - Componentes de Layout

**Propósito**: Componentes reutilizables para la estructura de la aplicación.

#### Navbar Principal
```python
def navbar_icons() -> rx.Component:
    """
    HEADER COMPLETAMENTE NUEVO - DISEÑO SIMPLE Y DIRECTO
    
    Características:
    - Responsive: Versión desktop y móvil
    - Logo clickeable que redirige a inicio
    - Navegación principal con iconos
    - Menú hamburguesa para móvil
    - Posición sticky en la parte superior
    """

def navbar_icons_item(text: str, icon: str, url: str) -> rx.Component:
    """
    Item individual del navbar desktop.
    
    Args:
        text: Texto del enlace
        icon: Icono a mostrar
        url: URL de destino
    
    Returns:
        rx.link: Enlace con icono y texto
    """
```

#### Menú Móvil
```python
def mobile_menu() -> rx.Component:
    """
    Menú desplegable para dispositivos móviles.
    
    Características:
    - Fondo semi-transparente que cierra el menú
    - Animación suave de entrada/salida
    - Mismos enlaces que el navbar desktop
    - Cierre automático al hacer click en enlace
    """

def mobile_menu_item(text: str, icon: str, url: str) -> rx.Component:
    """
    Item individual del menú móvil.
    
    Args:
        text: Texto del enlace
        icon: Icono a mostrar
        url: URL de destino
    
    Returns:
        rx.link: Enlace con icono y texto
    """
```

#### Modal de Login
```python
def login_dialog() -> rx.Component:
    """
    Modal de inicio de sesión.
    
    Características:
    - Formulario de login con validación
    - Manejo de errores de autenticación
    - Cierre automático al autenticarse
    - Redirección post-login
    """
```

#### Layout de Página
```python
def page_layout(*content):
    """
    Layout principal para todas las páginas.
    
    Args:
        *content: Contenido de la página
    
    Returns:
        rx.Component: Página completa con header, contenido y footer
    
    Características:
    - Header fijo con navegación
    - Menú móvil integrado
    - Modal de login integrado
    - Footer con información del proyecto
    - Responsive design
    """
```

---

## 📄 Páginas de la Aplicación

### 1. `pages/index.py` - Página de Inicio

**Propósito**: Landing page principal con información del proyecto y navegación.

**Componentes Principales**:
- Tarjetas de navegación con efectos hover
- Información del proyecto
- Enlaces a secciones principales

**Funcionalidades**:
- Efectos CSS personalizados con animaciones
- Diseño responsive (desktop/móvil)
- Navegación directa a instituciones y cursos

### 2. `pages/cursos.py` - Buscador de Cursos

**Propósito**: Página principal para buscar y filtrar cursos educativos.

**Componentes Principales**:
- Filtros múltiples (nivel, institución, lugar, requisitos)
- Búsqueda por texto libre
- Tabla de resultados con información detallada
- Sistema de paginación

**Funcionalidades**:
- Filtrado en tiempo real
- Cache inteligente de datos
- Progressive loading
- Responsive design

### 3. `pages/instituciones.py` - Galería de Instituciones

**Propósito**: Mostrar información de instituciones educativas y sus sedes.

**Componentes Principales**:
- Galería de tarjetas de instituciones
- Modal con detalles de institución
- Información de sedes por institución
- Filtro por ciudad

**Funcionalidades**:
- Vista de sedes como tarjetas individuales
- Modal con información detallada
- Navegación a cursos filtrados por institución
- Soporte para instituciones virtuales

### 4. `pages/admin.py` - Panel de Administración

**Propósito**: Gestión de cursos para usuarios autenticados.

**Componentes Principales**:
- Tabla de cursos de la institución
- Formulario de creación/edición de cursos
- Modal de confirmación de eliminación
- Filtros y búsqueda

**Funcionalidades**:
- CRUD completo de cursos
- Validación de formularios
- Aislamiento por institución
- Soporte para múltiples ciudades

### 5. `pages/admin_sedes.py` - Gestión de Sedes

**Propósito**: Gestión de sedes para usuarios autenticados.

**Componentes Principales**:
- Tabla de sedes de la institución
- Formulario de creación/edición de sedes
- Modal de confirmación de eliminación

**Funcionalidades**:
- CRUD completo de sedes
- Validación de formularios
- Aislamiento por institución

### 6. `pages/login.py` - Página de Login

**Propósito**: Página dedicada para inicio de sesión.

**Componentes Principales**:
- Formulario de autenticación
- Manejo de errores
- Redirección post-login

**Funcionalidades**:
- Validación de credenciales
- Mensajes de error descriptivos
- Redirección automática

### 7. `pages/info.py` - Información del Proyecto

**Propósito**: Página con información técnica y de contacto del proyecto.

**Componentes Principales**:
- Información del proyecto
- Detalles técnicos
- Información de contacto
- Enlaces útiles

---

## 🔧 Scripts de Automatización

### 1. `scripts/setup-env.sh` - Configuración de Entornos

**Propósito**: Configura automáticamente el entorno de desarrollo o producción.

**Funcionalidades**:
- Cambio entre entornos (desarrollo/producción)
- Configuración de variables de entorno
- Verificación de dependencias
- Limpieza de archivos temporales

### 2. `scripts/start-project.sh` - Inicio de Proyecto

**Propósito**: Inicia la aplicación en diferentes modos.

**Modos Disponibles**:
- `local`: Desarrollo local sin Docker
- `docker`: Desarrollo con Docker
- `production`: Modo producción
- `help`: Muestra ayuda

### 3. `scripts/deploy-to-vps.sh` - Despliegue Manual

**Propósito**: Despliega la aplicación al VPS de producción.

**Funcionalidades**:
- Sincronización de archivos via rsync
- Configuración de variables de entorno
- Reinicio de servicios
- Verificación de despliegue

### 4. `scripts/verify-production-setup.sh` - Verificación de Producción

**Propósito**: Verifica que la configuración de producción sea correcta.

**Verificaciones**:
- Variables de entorno
- Configuración de Docker
- Conectividad de servicios
- Permisos de archivos

---

## 📊 Relaciones entre Componentes

### Diagrama de Dependencias
```
saltoestudia.py
├── state.py
│   ├── database.py
│   │   ├── models.py
│   │   └── constants.py
│   └── theme.py
├── layout.py
│   └── state.py
└── pages/
    ├── index.py
    │   └── layout.py
    ├── cursos.py
    │   ├── state.py
    │   ├── theme.py
    │   └── layout.py
    ├── instituciones.py
    │   ├── state.py
    │   ├── theme.py
    │   └── layout.py
    ├── admin.py
    │   ├── state.py
    │   ├── theme.py
    │   └── layout.py
    ├── admin_sedes.py
    │   ├── state.py
    │   ├── theme.py
    │   └── layout.py
    ├── login.py
    │   ├── state.py
    │   └── layout.py
    └── info.py
        └── layout.py
```

### Flujo de Datos
1. **Usuario interactúa** con una página
2. **Página llama** a métodos del State
3. **State ejecuta** lógica de negocio
4. **State llama** a funciones de Database
5. **Database consulta** la base de datos
6. **Resultados fluyen** de vuelta a la UI

---

*Esta documentación se actualiza automáticamente con cada cambio en los componentes del sistema.* 