# ================================================================================
# ARCHIVO PRINCIPAL DE LA APLICACIÓN SALTO ESTUDIA
# ================================================================================
# 
# ⚠️ ADVERTENCIA CRÍTICA: Este proyecto SOLO se ejecuta en Docker
# 
# NO ejecutes 'reflex run' directamente. Usa siempre:
# docker compose -f docker-compose.desarrollo.yml up -d
# 
# Para más información, consulta DOCKER-ONLY.md
# 
# Este archivo es el punto de entrada principal del sistema Salto Estudia.
# Define la configuración global de la aplicación Reflex y gestiona las importaciones
# de todas las páginas del sistema.
#
# FUNCIONAMIENTO:
# - Configura la aplicación Reflex con estilos Bootstrap
# - Las páginas se registran automáticamente mediante el decorador @rx.page
# - No es necesario llamar a app.add_page() manualmente
#
# ARQUITECTURA DEL SISTEMA:
# - Frontend: Reflex (Python → React) con Bootstrap CSS
# - Backend: SQLModel + SQLite para persistencia
# - Autenticación: bcrypt para hash de contraseñas
# - Estado: Reflex State management para UI reactiva
# - CONTAINERIZACIÓN: Docker obligatorio para ejecución
# ================================================================================

import reflex as rx

# === IMPORTACIONES DE PÁGINAS ===
# Al importar estas páginas, se registran automáticamente en la aplicación
# gracias al decorador @rx.page que contienen
from .pages.index import index              # Página de inicio con información del proyecto
from .pages.instituciones import instituciones  # Galería de instituciones educativas
from .pages.cursos import cursos            # Buscador de cursos con filtros
from .pages.info import info                # Información adicional del proyecto
from .pages.admin import admin_page         # Panel de administración (requiere login)
from .pages.admin_sedes import admin_sedes_page  # Gestión de sedes (requiere login)
from .pages.login import login_page         # Página de inicio de sesión

# === IMPORTACIONES DE MODELOS ===
# Importar modelos para que SQLModel los reconozca y cree las tablas
from . import models

# === CONFIGURACIÓN DE LA APLICACIÓN ===
# Configuración principal de Reflex con Bootstrap CSS para estilos base
# Bootstrap proporciona componentes responsivos y estilos consistentes
app = rx.App(
    stylesheets=["https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css"]
)

# === REGISTRO AUTOMÁTICO DE PÁGINAS ===
# IMPORTANTE: NO es necesario llamar a app.add_page() para las páginas que usan 
# el decorador @rx.page. El decorador ya las registra automáticamente.
# 
# Intentar registrarlas manualmente generaría la advertencia:
# "redefined with the same component"
#
# Las páginas se registran con estas rutas:
# - / → index (página de inicio)
# - /instituciones → galería de instituciones
# - /cursos → buscador de cursos con filtros
# - /info → información del proyecto
# - /admin → panel administrativo (protegido)
# - /admin/sedes → gestión de sedes (protegido)
# - /login → formulario de inicio de sesión
#
# FLUJO DE NAVEGACIÓN:
# 1. Usuario accede a / (inicio)
# 2. Puede navegar a /instituciones o /cursos sin autenticación
# 3. Para acceder a /admin debe autenticarse en /login
# 4. Una vez autenticado, puede gestionar cursos de su institución
