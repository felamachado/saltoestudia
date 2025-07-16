# 📋 Changelog - Salto Estudia

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### 🚀 **Nuevas Características**
- **Scripts completamente no-interactivos** para VPS y entornos automatizados
- **Gestión automática de procesos** sin confirmaciones manuales
- **Compatibilidad mejorada** con CI/CD y despliegues automáticos

### 🔧 **Mejoras**
- **Eliminación de prompts interactivos** en todos los scripts
- **Detección automática de procesos anteriores** y terminación automática
- **Limpieza automática de puertos** sin preguntar al usuario
- **Actualización automática de alias** existentes
- **Mejor manejo de errores** y validaciones

### 🛠️ **Scripts Modificados**
- `scripts/arrancar_app.sh`: Eliminados prompts de confirmación
- `scripts/limpiar_puertos.sh`: Limpieza automática sin interacción
- `start.sh`: Validación mejorada y manejo de errores
- `install-alias.sh`: Actualización automática de alias existentes

### 📚 **Documentación**
- **README actualizado** con información sobre compatibilidad VPS
- **Sección de características** de scripts no-interactivos
- **Guía de solución de problemas** mejorada
- **Ejemplos de uso** para entornos automatizados

### 🎯 **Casos de Uso**
- **VPS sin interacción manual**
- **Entornos de CI/CD**
- **Despliegues automatizados**
- **Contenedores Docker**
- **Scripts de automatización**

## [1.2.1] - 2025-01-27

### 🔧 Mejorado
- **Scripts más robustos** para prevenir errores de carpeta incorrecta
- **Script global `start.sh`** que funciona desde cualquier carpeta
- **Mejor manejo de errores** con mensajes claros y soluciones
- **Detección de procesos existentes** para evitar conflictos
- **Documentación mejorada** con tabla de problemas comunes

### 🚀 Agregado
- **Script `install-alias.sh`** para instalar alias global `saltoestudia`
- **Múltiples opciones de arranque** para diferentes escenarios
- **Verificación automática** de carpeta correcta del proyecto
- **Guía de solución de problemas** en el README

### 🐛 Corregido
- **Error "rxconfig.py not found"** cuando se ejecuta desde carpeta incorrecta
- **Error "Script no encontrado"** cuando se ejecuta desde carpeta incorrecta
- **Conflictos de procesos** cuando ya hay Reflex corriendo

### 📚 Documentación
- **README actualizado** con opciones de arranque desde cualquier carpeta
- **Tabla de problemas comunes** y sus soluciones
- **Instrucciones claras** para cada método de arranque

## [1.2.0] - 2025-01-27

### 🚀 Agregado
- **Scripts de arranque automático** para resolver problemas de arranque intermitente
  - `scripts/arrancar_app.sh` - Arranque completo automático
  - `scripts/limpiar_puertos.sh` - Limpieza de puertos 8000 y 3000
  - `scripts/README.md` - Documentación de scripts
- **Documentación mejorada** con procedimiento definitivo para arrancar la app
- **Tabla de errores comunes** y sus soluciones
- **Checklist de verificación** antes de arrancar

### 🔧 Mejorado
- **README.md** completamente reorganizado y simplificado
- **Procedimiento de arranque** más claro y confiable
- **Compatibilidad VPS** mejorada con scripts automáticos
- **Manejo de errores** más robusto

### 🧹 Limpieza
- **Eliminados archivos innecesarios**:
  - Archivos de backup (*.backup*)
  - Archivos temporales (test-*.py, test-*.html)
  - Carpetas de caché (__pycache__, .web, .npm, .bun)
  - Archivos antiguos (dockerfile.old, start.sh.old)
- **Estructura del proyecto** más limpia y organizada

### 🔒 Seguridad
- **Verificación de seguridad** completada
- **Gitignore mejorado** para proteger información sensible
- **Documentación de seguridad** actualizada

### 📚 Documentación
- **README.md** completamente reescrito y simplificado
- **Procedimiento definitivo** para arrancar la aplicación
- **Guía de errores comunes** y soluciones
- **Documentación de scripts** en `scripts/README.md`

## [1.1.0] - 2025-01-26

### 🚀 Agregado
- **Sistema de autenticación** con bcrypt
- **Panel administrativo** por institución
- **Gestión de instituciones** educativas
- **Buscador de cursos** con filtros avanzados
- **Diseño responsive** con AG Grid

### 🔧 Mejorado
- **Arquitectura Docker** dual (desarrollo/producción)
- **Despliegue VPS** automatizado con Traefik
- **Base de datos SQLite** optimizada
- **Sistema de migraciones** con Alembic

### 🐛 Corregido
- **Problemas de WebSocket** en producción
- **Configuración SSL** con Let's Encrypt
- **Proxy reverso** Traefik configurado correctamente

## [1.0.0] - 2025-01-25

### 🎉 **Lanzamiento Inicial**
- **Plataforma educativa completa** con Reflex
- **Sistema de gestión de cursos** y estudiantes
- **Interfaz administrativa** integrada
- **Base de datos SQLite** con Alembic
- **Despliegue automatizado** en VPS Oracle Cloud

### 🚀 **Características Principales**
- **Frontend React** con Reflex
- **Backend Python** con FastAPI
- **Base de datos** con SQLAlchemy y Alembic
- **Autenticación** y autorización
- **Panel de administración** completo

### 🛠️ **Scripts de Desarrollo**
- `scripts/arrancar_app.sh`: Arranque completo con limpieza de puertos
- `scripts/limpiar_puertos.sh`: Limpieza de puertos ocupados
- `start.sh`: Script global desde cualquier ubicación
- `install-alias.sh`: Instalación de alias global

### 🐳 **Docker**
- **Contenedor de producción** optimizado
- **Configuración Traefik** para proxy reverso
- **SSL automático** con Let's Encrypt
- **Despliegue automatizado** con GitHub Actions

### 🌐 **Despliegue**
- **VPS Oracle Cloud** configurado
- **Dominio personalizado**: saltoestudia.infra.com.uy
- **SSL automático** y seguro
- **Backup automático** de datos

---

## 🔄 Tipos de Cambios

- **🚀 Agregado** - Nuevas características
- **🔧 Mejorado** - Mejoras en funcionalidades existentes
- **🐛 Corregido** - Corrección de bugs
- **🧹 Limpieza** - Limpieza de código y archivos
- **🔒 Seguridad** - Mejoras de seguridad
- **📚 Documentación** - Actualizaciones de documentación
- **⚡ Performance** - Mejoras de rendimiento
- **♻️ Refactor** - Refactorización de código

## 📝 Notas de Desarrollo

### Versiones
- **MAJOR.MINOR.PATCH**
- **MAJOR**: Cambios incompatibles con versiones anteriores
- **MINOR**: Nuevas funcionalidades compatibles
- **PATCH**: Correcciones de bugs compatibles

### Convenciones
- Fechas en formato YYYY-MM-DD
- Emojis para categorizar cambios
- Descripción clara de cada cambio
- Referencias a issues cuando aplique 

---

**Desarrollado con ❤️ para la educación** 