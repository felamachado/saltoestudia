# 🔧 Scripts de Utilidad - Salto Estudia

Esta carpeta contiene scripts útiles para el desarrollo y mantenimiento del proyecto.

## 📋 Lista de Scripts

### 🧹 `reflex-clean.sh`
**Propósito:** Script para limpiar y ejecutar Reflex (DEPRECADO - usar Docker).

**Uso:**
```bash
./scripts/reflex-clean.sh
```

**Nota:** Este script está deprecado. El proyecto ahora se ejecuta exclusivamente en Docker.

### 🚀 `start-project.sh`
**Propósito:** Arranque completo de la aplicación en Docker.

**Uso:**
```bash
./scripts/start-project.sh docker
```

**Características:**
- Verifica que estés en la carpeta correcta del proyecto
- Verifica que Docker esté instalado
- Construye y levanta contenedores automáticamente
- Arranca la aplicación con configuración optimizada
- Muestra las URLs de acceso

### 🔒 `security_check.sh`
**Propósito:** Verificaciones de seguridad del proyecto.

**Uso:**
```bash
./scripts/security_check.sh
```

## 🛠️ Instalación y Configuración

### Dar permisos de ejecución
```bash
chmod +x scripts/*.sh
```

### Verificar que funcionan
```bash
# Probar arranque completo
./scripts/start-project.sh docker
```

## 🔧 Compatibilidad

Todos los scripts están diseñados para funcionar en:
- ✅ Ubuntu/Debian
- ✅ CentOS/RHEL
- ✅ Amazon Linux
- ✅ Cualquier VPS con Linux

### Requisitos
- `bash` (incluido por defecto)
- `lsof` (se instala automáticamente si falta)
- `ps` (incluido por defecto)

## 🚨 Solución de Problemas

### Error: "Permission denied"
```bash
chmod +x scripts/start-project.sh
```

### Error: "lsof not found"
El script instalará `lsof` automáticamente. Si falla:
```bash
# Ubuntu/Debian
sudo apt-get install lsof

# CentOS/RHEL
sudo yum install lsof
```

### Error: "rxconfig.py not found"
Asegúrate de ejecutar desde la carpeta raíz del proyecto:
```bash
cd ~/Escritorio/Proyectos/saltoestudia
./scripts/arrancar_app.sh
```

## 📝 Notas de Desarrollo

### Agregar nuevos scripts
1. Crear el archivo en `scripts/`
2. Agregar shebang: `#!/bin/bash`
3. Dar permisos: `chmod +x scripts/nuevo_script.sh`
4. Documentar en este README

### Estructura recomendada
```bash
#!/bin/bash

# =============================================================================
# Descripción del script
# =============================================================================
# 
# Propósito y uso del script
#
# Uso: ./scripts/nombre_script.sh
# =============================================================================

set -e  # Salir si hay error

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Funciones de output
print_status() { echo -e "${BLUE}[INFO]${NC} $1"; }
print_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
print_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
print_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Código del script...
```

## 📞 Soporte

Si tienes problemas con los scripts:
1. Verifica que tienes permisos de ejecución
2. Asegúrate de estar en la carpeta correcta
3. Revisa los mensajes de error
4. Consulta la documentación principal en `../README.md` 