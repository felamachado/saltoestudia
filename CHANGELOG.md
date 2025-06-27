# 📋 Changelog - Salto Estudia

Todos los cambios notables en este proyecto serán documentados en este archivo.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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

### 🚀 Lanzamiento inicial
- **Aplicación base** con Reflex
- **Estructura del proyecto** definida
- **Configuración Docker** básica
- **Despliegue inicial** en VPS

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