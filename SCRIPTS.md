# 🔧 Scripts de Automatización - Salto Estudia

## 📋 Resumen

Este documento describe todos los scripts de automatización incluidos en el proyecto Salto Estudia. Estos scripts facilitan el desarrollo, despliegue, mantenimiento y solución de problemas del sistema.

## 🚀 Scripts Principales

### 1. `scripts/check-docker-only.sh` - Verificación Docker Only ⚠️

**Propósito**: Verifica que el proyecto se ejecute solo en Docker y previene el uso de Reflex nativo.

**Uso**:
```bash
./scripts/check-docker-only.sh
```

**Funcionalidades**:
- Verifica que Docker esté instalado y ejecutándose
- Comprueba que docker-compose esté disponible
- Valida archivos de configuración necesarios
- Verifica que los puertos necesarios estén libres
- Muestra advertencias si se intenta usar Reflex nativo

**Verificaciones**:
- ✅ Docker instalado y ejecutándose
- ✅ docker-compose disponible
- ✅ Archivos de configuración presentes
- ✅ Puertos 3000, 8000, 5432 libres
- ❌ Previene uso de `reflex run`

**Mensajes de Error**:
- Muestra advertencia clara si se intenta usar Reflex nativo
- Proporciona comandos correctos para usar Docker
- Enlaza a documentación relevante

---

### 2. `scripts/setup-env.sh` - Configuración de Entornos

**Propósito**: Configura automáticamente el entorno de desarrollo o producción.

**Uso**:
```bash
./scripts/setup-env.sh [desarrollo|produccion]
```

**Funcionalidades**:
- Cambio entre entornos (desarrollo/producción)
- Configuración de variables de entorno
- Verificación de dependencias
- Limpieza de archivos temporales
- Configuración de permisos

**Proceso**:
1. **Validación**: Verifica que el entorno especificado sea válido
2. **Backup**: Crea backup de configuración actual
3. **Configuración**: Aplica configuración del entorno seleccionado
4. **Verificación**: Valida que la configuración sea correcta
5. **Limpieza**: Elimina archivos temporales

**Archivos Afectados**:
- `docker-compose.yml` (enlace simbólico)
- Variables de entorno
- Permisos de archivos

---

### 2. `scripts/start-project.sh` - Inicio de Proyecto

**Propósito**: Inicia la aplicación en diferentes modos de operación.

**Uso**:
```bash
./scripts/start-project.sh [local|docker|production|help]
```

**Modos Disponibles**:

#### Modo `local`
```bash
./scripts/start-project.sh local
```
- Inicia Reflex en modo desarrollo local
- Sin Docker, directamente en el sistema
- Hot reload activado
- Puerto 3000 (frontend) y 8000 (backend)

#### Modo `docker`
```bash
./scripts/start-project.sh docker
```
- Inicia con Docker Compose
- Modo desarrollo con volúmenes montados
- Hot reload activado
- Logs en tiempo real

#### Modo `production`
```bash
./scripts/start-project.sh production
```
- Inicia en modo producción
- Configuración optimizada
- Sin hot reload
- Logs estructurados

#### Modo `help`
```bash
./scripts/start-project.sh help
```
- Muestra ayuda detallada
- Lista todos los modos disponibles
- Explica parámetros

**Funcionalidades**:
- Detección automática de entorno
- Verificación de dependencias
- Limpieza de procesos anteriores
- Configuración de puertos
- Manejo de errores

---

### 3. `scripts/deploy-to-vps.sh` - Despliegue Manual

**Propósito**: Despliega la aplicación al VPS de producción.

**Uso**:
```bash
./scripts/deploy-to-vps.sh
```

**Requisitos**:
- Acceso SSH al VPS
- Clave SSH configurada
- Variables de entorno configuradas

**Proceso de Despliegue**:
1. **Verificación**: Comprueba conectividad con VPS
2. **Backup**: Crea backup de la aplicación actual
3. **Sincronización**: Transfiere archivos via rsync
4. **Configuración**: Aplica variables de entorno
5. **Reinicio**: Reinicia servicios Docker
6. **Verificación**: Comprueba que la aplicación funcione

**Archivos Transferidos**:
- Código fuente completo
- Archivos de configuración
- Scripts de automatización
- Documentación

**Excluidos**:
- Archivos temporales
- Logs
- Base de datos local
- Archivos de desarrollo

---

### 4. `scripts/verify-production-setup.sh` - Verificación de Producción

**Propósito**: Verifica que la configuración de producción sea correcta.

**Uso**:
```bash
./scripts/verify-production-setup.sh
```

**Verificaciones Realizadas**:

#### Variables de Entorno
- `DATABASE_URL`: URL de base de datos
- `REFLEX_DB_URL`: URL de base de datos Reflex
- `PYTHONPATH`: Path de Python
- Variables de autenticación

#### Configuración de Docker
- Docker Compose configurado
- Imágenes construidas
- Contenedores ejecutándose
- Redes configuradas

#### Conectividad de Servicios
- Frontend accesible (puerto 3000)
- Backend accesible (puerto 8000)
- Base de datos conectable
- WebSocket funcionando

#### Permisos de Archivos
- Base de datos con permisos correctos
- Logs escribibles
- Archivos de configuración legibles

**Salida**:
- Reporte detallado de verificaciones
- Errores encontrados
- Recomendaciones de corrección

---

## 🛠️ Scripts de Mantenimiento

### 5. `scripts/verify-setup.sh` - Verificación Completa

**Propósito**: Verificación exhaustiva de todo el setup del proyecto.

**Uso**:
```bash
./scripts/verify-setup.sh
```

**Verificaciones**:
- Dependencias de Python
- Dependencias de Node.js
- Configuración de Docker
- Variables de entorno
- Base de datos
- Permisos de archivos
- Conectividad de servicios
- Funcionalidades básicas

**Módulos de Verificación**:
- **Dependencies**: Verifica pip, npm, docker
- **Configuration**: Verifica archivos de configuración
- **Database**: Verifica conexión y estructura
- **Services**: Verifica servicios en ejecución
- **Functionality**: Prueba funcionalidades básicas

---

### 6. `scripts/reset-project.sh` - Reset Completo

**Propósito**: Resetea completamente el proyecto a un estado limpio.

**Uso**:
```bash
./scripts/reset-project.sh
```

**⚠️ ADVERTENCIA**: Este script elimina todos los datos locales.

**Proceso**:
1. **Parada**: Detiene todos los servicios
2. **Limpieza**: Elimina contenedores, volúmenes, redes
3. **Reset**: Elimina archivos temporales y cache
4. **Reconstrucción**: Reconstruye imágenes Docker
5. **Inicialización**: Inicializa base de datos
6. **Seed**: Carga datos de ejemplo

**Archivos Eliminados**:
- Contenedores Docker
- Volúmenes Docker
- Redes Docker
- Cache de Reflex
- Archivos temporales
- Base de datos local

---

### 7. `scripts/verify-env.sh` - Verificación de Variables de Entorno

**Propósito**: Verifica que el archivo `.env` esté configurado correctamente para el entorno especificado.

**Uso**:
```bash
./scripts/verify-env.sh [local|production]
```

**Modos Disponibles**:

#### Modo `local`
```bash
./scripts/verify-env.sh local
```
- Verifica configuración para desarrollo local
- Valida URLs de SQLite
- Comprueba contraseñas de usuarios
- Ideal para desarrollo

#### Modo `production`
```bash
./scripts/verify-env.sh production
```
- Verifica configuración para producción
- Valida URLs de PostgreSQL
- Comprueba DB_PASSWORD
- Verifica REFLEX_ENV=production

**Verificaciones Realizadas**:
- Existencia del archivo `.env`
- Configuración de base de datos (SQLite/PostgreSQL)
- Variables de contraseñas de usuarios
- Configuración de entorno (desarrollo/producción)

**Ejemplo de Salida**:
```bash
🔍 Verificando configuración del archivo .env...
✅ Archivo .env encontrado
🔧 Verificando configuración LOCAL (SQLite)...
✅ DATABASE_URL configurado para SQLite
✅ REFLEX_DB_URL configurado para SQLite
🔑 Verificando contraseñas de usuarios...
✅ DEFAULT_SEED_PASSWORD configurado
✅ CENUR_PASSWORD configurado
```

### 8. `scripts/diagnose-problems.sh` - Diagnóstico de Problemas

**Propósito**: Diagnostica problemas comunes del sistema.

**Uso**:
```bash
./scripts/diagnose-problems.sh
```

**Diagnósticos Realizados**:

#### Problemas de Red
- Puertos ocupados
- Firewall bloqueando
- DNS no resolviendo
- Proxy configurado

#### Problemas de Docker
- Docker no ejecutándose
- Imágenes corruptas
- Contenedores colgados
- Recursos insuficientes

#### Problemas de Base de Datos
- Archivo corrupto
- Permisos incorrectos
- Conexión fallida
- Esquema inválido

#### Problemas de Aplicación
- Dependencias faltantes
- Variables de entorno incorrectas
- Logs de error
- Performance degradada

**Salida**:
- Reporte detallado de problemas
- Soluciones recomendadas
- Comandos de corrección

---

### 8. `scripts/security_check.sh` - Verificación de Seguridad

**Propósito**: Verifica la seguridad del proyecto.

**Uso**:
```bash
./scripts/security_check.sh
```

**Verificaciones de Seguridad**:

#### Archivos Sensibles
- Credenciales en código
- Archivos .env en Git
- Claves privadas expuestas
- Logs con información sensible

#### Configuración de Seguridad
- Permisos de archivos
- Configuración de Docker
- Variables de entorno
- Headers de seguridad

#### Dependencias
- Vulnerabilidades conocidas
- Versiones desactualizadas
- Dependencias no utilizadas
- Licencias problemáticas

**Salida**:
- Reporte de vulnerabilidades
- Recomendaciones de seguridad
- Priorización de problemas

---

### 9. `scripts/reflex-clean.sh` - Limpieza de Reflex

**Propósito**: Limpia archivos temporales de Reflex.

**Uso**:
```bash
./scripts/reflex-clean.sh
```

**Archivos Limpiados**:
- Cache de Reflex
- Archivos temporales
- Logs antiguos
- Builds obsoletos

**Funcionalidades**:
- Limpieza selectiva
- Preservación de datos importantes
- Verificación post-limpieza
- Log de acciones realizadas

---

## 📊 Scripts de Utilidad

### 10. `scripts/README.md` - Documentación de Scripts

**Propósito**: Documentación específica de los scripts.

**Contenido**:
- Descripción de cada script
- Ejemplos de uso
- Parámetros disponibles
- Casos de uso comunes
- Solución de problemas

---

## 🔄 Workflow de Scripts

### Flujo de Desarrollo Típico

```bash
# 1. Configurar entorno
./scripts/setup-env.sh desarrollo

# 2. Verificar setup
./scripts/verify-setup.sh

# 3. Iniciar proyecto
./scripts/start-project.sh docker

# 4. Desarrollo...
# (cambios en código)

# 5. Si hay problemas
./scripts/diagnose-problems.sh

# 6. Si necesitas reset
./scripts/reset-project.sh
```

### Flujo de Producción

```bash
# 1. Configurar entorno
./scripts/setup-env.sh produccion

# 2. Verificar producción
./scripts/verify-production-setup.sh

# 3. Desplegar
./scripts/deploy-to-vps.sh

# 4. Verificar despliegue
./scripts/verify-production-setup.sh
```

---

## 🛡️ Seguridad de Scripts

### Buenas Prácticas Implementadas

#### Validación de Entrada
- Verificación de parámetros
- Sanitización de inputs
- Validación de rutas
- Comprobación de permisos

#### Manejo de Errores
- Captura de errores
- Logs detallados
- Rollback automático
- Mensajes informativos

#### Permisos
- Verificación de permisos antes de ejecutar
- Uso de sudo solo cuando es necesario
- Preservación de permisos originales
- Log de cambios de permisos

#### Backup
- Backup automático antes de cambios críticos
- Preservación de datos importantes
- Rollback en caso de error
- Verificación de integridad

---

## 📈 Monitoreo y Logs

### Sistema de Logs

Todos los scripts implementan un sistema de logs consistente:

#### Niveles de Log
- **INFO**: Información general
- **WARNING**: Advertencias
- **ERROR**: Errores críticos
- **DEBUG**: Información de depuración

#### Formato de Logs
```bash
[2024-01-15 10:30:45] [INFO] Iniciando script setup-env.sh
[2024-01-15 10:30:46] [INFO] Configurando entorno: desarrollo
[2024-01-15 10:30:47] [SUCCESS] Entorno configurado correctamente
```

#### Ubicación de Logs
- **Desarrollo**: `./logs/scripts/`
- **Producción**: `/var/log/saltoestudia/scripts/`
- **Rotación**: Automática diaria
- **Retención**: 30 días

---

## 🔧 Personalización de Scripts

### Variables de Configuración

Los scripts pueden personalizarse mediante variables de entorno:

```bash
# Configuración de VPS
VPS_HOST=150.230.30.198
VPS_USER=ubuntu
VPS_PATH=/home/ubuntu/saltoestudia

# Configuración de puertos
FRONTEND_PORT=3000
BACKEND_PORT=8000

# Configuración de base de datos
DATABASE_PATH=./data/saltoestudia.db
```

### Archivos de Configuración

- **`scripts/config.sh`**: Configuración global de scripts
- **`scripts/functions.sh`**: Funciones compartidas
- **`scripts/constants.sh`**: Constantes y valores por defecto

---

## 🐛 Solución de Problemas Comunes

### Script no ejecutable
```bash
chmod +x scripts/*.sh
```

### Error de permisos
```bash
sudo chown -R $USER:$USER .
chmod 755 scripts/
```

### Docker no disponible
```bash
# Verificar Docker
docker --version
docker-compose --version

# Instalar si es necesario
sudo apt-get install docker.io docker-compose
```

### Variables de entorno no cargadas
```bash
# Verificar archivo .env
ls -la .env

# Cargar manualmente
source .env
```

---

## 📚 Referencias

### Documentación Relacionada
- **`DEPLOYMENT.md`**: Guía de despliegue
- **`ENTORNOS.md`**: Configuración de entornos
- **`TROUBLESHOOTING.md`**: Solución de problemas
- **`ARCHITECTURE.md`**: Arquitectura del sistema

### Comandos Útiles
```bash
# Ver logs de un script específico
tail -f logs/scripts/setup-env.log

# Ejecutar script con debug
DEBUG=1 ./scripts/setup-env.sh desarrollo

# Verificar sintaxis de script
bash -n scripts/setup-env.sh

# Ejecutar con trace
bash -x scripts/setup-env.sh desarrollo
```

---

*Esta documentación se actualiza automáticamente con cada cambio en los scripts del sistema.* 