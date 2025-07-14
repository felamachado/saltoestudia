# 🎓 Salto Estudia

Sistema de gestión de cursos e instituciones educativas de Salto, Uruguay.

Desarrollado con **Reflex** (Python) + **SQLite** + **Docker**, incluye gestión completa de cursos, instituciones y panel administrativo con autenticación.

**✨ En producción:** https://saltoestudia.infra.com.uy

## ✨ Características

- 🎯 **Buscador de cursos** con filtros avanzados
- 🏛️ **Gestión de instituciones** educativas
- 👨‍💼 **Panel administrativo** por institución
- 🔒 **Autenticación segura** con bcrypt
- 📱 **Diseño responsive** con AG Grid
- 🗄️ **Base de datos SQLite** (sin dependencias externas)
- 🐳 **Docker optimizado** con hot-reload
- 🚀 **Despliegue VPS automatizado** con Traefik

## 🚀 **Arranque Rápido**

### **Opción 1: Comando Directo (Recomendado)**
```bash
# Desde cualquier carpeta
~/Escritorio/Proyectos/saltoestudia/scripts/arrancar_app.sh

# O si estás en la carpeta del proyecto
./scripts/arrancar_app.sh
```

### **Opción 2: Alias Global (Más Fácil)**
```bash
# Instalar alias (solo una vez)
cd ~/Escritorio/Proyectos/saltoestudia
./install-alias.sh

# Usar desde cualquier carpeta
saltoestudia
```

### **Opción 3: Script Global**
```bash
# Desde cualquier carpeta
~/Escritorio/Proyectos/saltoestudia/start.sh
```

## 🔧 **Características de los Scripts**

### ✅ **Completamente No-Interactivos**
- **Funcionan en VPS y entornos automatizados**
- **No requieren confirmaciones manuales**
- **Ideal para CI/CD y despliegues automáticos**

### 🛡️ **Gestión Automática de Procesos**
- **Detecta y detiene procesos anteriores automáticamente**
- **Limpia puertos ocupados sin preguntar**
- **Verifica dependencias e instala si es necesario**

### 📍 **Ejecución desde Cualquier Ubicación**
- **No necesitas navegar al directorio del proyecto**
- **Scripts detectan automáticamente la ubicación correcta**
- **Funcionan desde cualquier carpeta del sistema**

## 🌐 **Acceso a la Aplicación**

Una vez arrancada, la aplicación estará disponible en:

- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:8000  
- **Admin**: http://localhost:3000/admin

## 🛠️ **Scripts Disponibles**

### **`scripts/arrancar_app.sh`**
Script principal que combina limpieza de puertos y arranque de Reflex.

**Características:**
- ✅ Limpia puertos 3000 y 8000 automáticamente
- ✅ Detiene procesos de Reflex anteriores
- ✅ Verifica dependencias (instala Reflex si es necesario)
- ✅ Arranca con configuración optimizada
- ✅ Funciona desde cualquier carpeta

### **`scripts/limpiar_puertos.sh`**
Limpia puertos ocupados sin interacción manual.

**Características:**
- ✅ Mata procesos en puertos 3000 y 8000 automáticamente
- ✅ Muestra información detallada de procesos
- ✅ Verificación post-limpieza
- ✅ Compatible con VPS y entornos automatizados

### **`start.sh`**
Script global que funciona desde cualquier ubicación.

**Características:**
- ✅ Detecta automáticamente la ubicación del proyecto
- ✅ Redirige al script de arranque principal
- ✅ Validación de estructura del proyecto

### **`install-alias.sh`**
Instala un alias global para facilitar el arranque.

**Características:**
- ✅ Detecta automáticamente el shell (bash/zsh)
- ✅ Instala alias en el archivo de configuración correcto
- ✅ Actualiza alias existentes automáticamente
- ✅ Recarga configuración del shell

## 🔍 **Solución de Problemas**

### **Error: "rxconfig.py not found"**
```bash
# Solución: Navega al directorio correcto
cd ~/Escritorio/Proyectos/saltoestudia
./scripts/arrancar_app.sh
```

### **Error: "Puerto ya en uso"**
```bash
# Los scripts limpian automáticamente, pero si persiste:
./scripts/limpiar_puertos.sh
```

### **Error: "Reflex no está instalado"**
```bash
# Los scripts instalan automáticamente, pero si falla:
pip install reflex
```

### **Error: "Permisos denegados"**
```bash
# Dar permisos de ejecución
chmod +x scripts/*.sh
chmod +x *.sh
```

## 🐳 **Docker (Producción)**

Para el entorno de producción, usa Docker:

```bash
# Construir imagen
docker build -t saltoestudia .

# Ejecutar contenedor
docker run -p 3000:3000 -p 8000:8000 saltoestudia
```

**Nota**: El contenedor Docker está configurado para producción y no expone puertos para desarrollo local. Para desarrollo, usa los scripts locales.

## 📋 **Requisitos del Sistema**

- **Python 3.8+**
- **pip**
- **lsof** (normalmente instalado por defecto)
- **bash** o **zsh**

## 🔄 **Actualizaciones**

Los scripts se actualizan automáticamente con el proyecto. Para forzar una actualización:

```bash
# Reinstalar alias
./install-alias.sh

# O limpiar y reinstalar
rm ~/.zshrc  # (hacer backup antes)
./install-alias.sh
```

## 📞 **Soporte**

Si encuentras problemas:

1. **Verifica que estés en la carpeta correcta**
2. **Ejecuta el script de limpieza manualmente**
3. **Revisa los logs de error**
4. **Asegúrate de tener permisos de ejecución**

---

**Desarrollado con ❤️ para la educación**

## 🏗️ Arquitectura

### 📂 Estructura del Proyecto

```
saltoestudia/
├── saltoestudia/                   # 🐍 Código fuente principal
│   ├── pages/                      # 📄 Páginas de la aplicación
│   │   ├── index.py                # 🏠 Página principal
│   │   ├── cursos.py               # 🎓 Buscador de cursos
│   │   ├── instituciones.py        # 🏛️ Galería de instituciones
│   │   ├── admin.py                # 👨‍💼 Panel administrativo
│   │   └── login.py                # 🔐 Autenticación
│   ├── models.py                   # 🗄️ Modelos de base de datos
│   ├── database.py                 # 🔌 Operaciones CRUD
│   ├── state.py                    # 📊 Estado global de Reflex
│   └── theme.py                    # 🎨 Sistema de diseño centralizado
├── assets/                         # 🖼️ Recursos estáticos (logos, etc)
├── data/                           # 📁 Base de datos SQLite
├── scripts/                        # 🔧 Scripts de utilidad
│   ├── arrancar_app.sh            # 🚀 Arranque completo
│   ├── limpiar_puertos.sh         # 🧹 Limpieza de puertos
│   └── security_check.sh          # 🔒 Verificaciones de seguridad
├── alembic/                        # 🔄 Migraciones de base de datos
├── dockerfile                      # 🐳 Imagen Docker para desarrollo
├── dockerfile.production           # 🚀 Dockerfile optimizado para VPS
├── docker-compose.yml              # 🐳 Compose para desarrollo local
├── docker-compose.production.yml   # ⚙️ Compose con configuración Traefik
├── deploy-to-vps.sh               # 🌐 Script despliegue automatizado
├── init_db.py                      # 🗄️ Inicialización de tablas
├── seed.py                         # 🌱 Datos iniciales
├── requirements.txt                # 📦 Dependencias Python
└── rxconfig.py                     # ⚙️ Configuración Reflex
```

## 🧹 Procedimiento Definitivo para Arrancar la App

**Problema común:** Cuando bajas la app y quieres volver a levantarla, a veces no arranca correctamente (errores de WebSocket, puertos ocupados, etc.).

**Solución definitiva:** Usar el script de arranque automático.

### 🚀 Opción 1: Script de Arranque Completo (Recomendado)

```bash
cd ~/Escritorio/Proyectos/saltoestudia
./scripts/arrancar_app.sh
```

**Este script hace todo automáticamente:**
- ✅ Verifica que estés en la carpeta correcta
- ✅ Ejecuta la limpieza de puertos
- ✅ Verifica que Reflex esté instalado
- ✅ Arranca la aplicación con configuración optimizada
- ✅ Te muestra las URLs donde acceder

### 🔧 Opción 2: Limpieza + Arranque Manual

```bash
cd ~/Escritorio/Proyectos/saltoestudia
./scripts/limpiar_puertos.sh
reflex run --backend-host 0.0.0.0 --backend-port 8000 --frontend-port 3000
```

### 🚨 Errores Comunes y Soluciones

| Error | Causa | Solución |
|-------|-------|----------|
| `rxconfig.py not found` | Ejecutando desde carpeta incorrecta | `cd ~/Escritorio/Proyectos/saltoestudia` |
| `WebSocket connection failed` | Puerto 8000 ocupado | Ejecutar `./scripts/limpiar_puertos.sh` |
| `404 /_event` | Backend no arrancó correctamente | Verificar puertos y carpeta correcta |
| `Address already in use` | Proceso previo ocupando puerto | Limpiar puertos antes de arrancar |

## 🗄️ Base de Datos

### SQLite (Sin configuración)
- **Archivo:** `./data/saltoestudia.db`
- **Inicialización:** Automática al primer arranque
- **Datos de ejemplo:** Se cargan automáticamente
- **Respaldos:** Simples archivos `.db`

### Respaldos
```bash
# Crear respaldo local
cp data/saltoestudia.db backup_$(date +%Y%m%d_%H%M%S).db

# Descargar backup desde VPS
scp ubuntu@150.230.30.198:/srv/docker/saltoestudia/data/saltoestudia.db backup_vps_$(date +%Y%m%d_%H%M%S).db

# Restaurar desde respaldo
cp backup_20241223_120000.db data/saltoestudia.db
```

## 🔐 Seguridad

### Autenticación
- **Sistema:** bcrypt + sesiones seguras
- **Usuarios por defecto:** Uno por institución
- **Contraseñas:** Configurables via variables de entorno

### Variables de Entorno (Opcional)

```bash
# Crear .env para contraseñas personalizadas
echo 'DEFAULT_SEED_PASSWORD=tu_contraseña_segura' > .env
echo 'DATABASE_URL=sqlite:///./data/saltoestudia.db' >> .env
```

**Nota:** El proyecto funciona sin `.env` usando contraseñas por defecto.

## 📦 Despliegue en Producción

### VPS Oracle Cloud (Recomendado)

```bash
# Despliegue automatizado con Traefik
./deploy-to-vps.sh
```

**Características:**
- ✅ **SSL automático** con Let's Encrypt
- ✅ **WebSocket** funcionando (`wss://`)
- ✅ **Proxy reverso** Traefik configurado
- ✅ **Backup automático** antes de cada despliegue
- ✅ **Monitoreo** integrado

### Lista de Verificación Producción

- [ ] ✅ Cambiar contraseñas por defecto (crear `.env`)
- [ ] ✅ Configurar HTTPS (nginx/traefik)
- [ ] ✅ Configurar respaldos automáticos de SQLite
- [ ] ✅ Monitorear logs con `docker logs -f`
- [ ] ✅ Actualizar dependencias regularmente

## 🤝 Contribuir

1. Fork el proyecto
2. Crear rama: `git checkout -b feature/nueva-caracteristica`
3. Commit cambios: `git commit -m 'Agregar nueva característica'`
4. Push: `git push origin feature/nueva-caracteristica`
5. Crear Pull Request

## 📄 Licencia

MIT License - ver [LICENSE](LICENSE) para detalles.

## 📞 Contacto

- **Proyecto:** Salto Estudia
- **GitHub:** https://github.com/felamachado/saltoestudia
- **Demo:** https://saltoestudia.infra.com.uy
- **Ubicación:** Salto, Uruguay
- **Año:** 2025

---

## 🎯 Tecnologías

- **Backend:** Python + Reflex + SQLAlchemy
- **Frontend:** React (generado por Reflex)
- **Base de Datos:** SQLite
- **Containerización:** Docker
- **Proxy Reverso:** Traefik (producción VPS)
- **UI Components:** AG Grid + Chakra UI
- **Autenticación:** bcrypt + sesiones
- **SSL:** Let's Encrypt automático

## Extras y Consideraciones

### 🧹 Procedimiento Definitivo para Arrancar la App

**Problema común:** Cuando bajas la app y quieres volver a levantarla, a veces no arranca correctamente (errores de WebSocket, puertos ocupados, etc.).

**Solución definitiva:** Usar el script de limpieza automática.

#### 🔧 Opción 1: Script Automático (Recomendado)

```bash
# 1. Navega a la carpeta del proyecto
cd ~/Escritorio/Proyectos/saltoestudia

# 2. Ejecuta el script de limpieza
./scripts/limpiar_puertos.sh

# 3. Arranca Reflex
reflex run --backend-host 0.0.0.0 --backend-port 8000 --frontend-port 3000
```

**El script automáticamente:**
- ✅ Detecta procesos ocupando puertos 8000 y 3000
- ✅ Te muestra qué procesos encontró
- ✅ Te pregunta si quieres matarlos
- ✅ Verifica que los puertos queden libres
- ✅ Te da los próximos pasos

#### 🚀 Opción 1.5: Script de Arranque Completo (Más Fácil)

```bash
# Un solo comando hace todo:
./scripts/arrancar_app.sh
```

**Este script hace todo automáticamente:**
- ✅ Verifica que estés en la carpeta correcta
- ✅ Ejecuta la limpieza de puertos
- ✅ Verifica que Reflex esté instalado
- ✅ Arranca la aplicación con la configuración correcta
- ✅ Te muestra las URLs donde acceder

#### 🔧 Opción 2: Limpieza Manual

Si prefieres hacerlo manualmente:

```bash
# 1. Cierra todos los procesos previos
pkill -f reflex
pkill -f "python3 -m http.server"

# 2. Verifica que los puertos estén libres
lsof -i :8000 || echo "Puerto 8000 libre"
lsof -i :3000 || echo "Puerto 3000 libre"

# 3. Navega a la carpeta del proyecto
cd ~/Escritorio/Proyectos/saltoestudia

# 4. Arranca Reflex
reflex run --backend-host 0.0.0.0 --backend-port 8000 --frontend-port 3000
```

### 🚨 Errores Comunes y Soluciones

| Error | Causa | Solución |
|-------|-------|----------|
| `rxconfig.py not found` | Ejecutando desde carpeta incorrecta | `cd ~/Escritorio/Proyectos/saltoestudia` |
| `WebSocket connection failed` | Puerto 8000 ocupado | Ejecutar `./scripts/limpiar_puertos.sh` |
| `404 /_event` | Backend no arrancó correctamente | Verificar puertos y carpeta correcta |
| `Address already in use` | Proceso previo ocupando puerto | Limpiar puertos antes de arrancar |

### 📋 Checklist de Arranque

Antes de arrancar Reflex, verifica:

- [ ] ✅ Estás en la carpeta correcta (`~/Escritorio/Proyectos/saltoestudia`)
- [ ] ✅ Los puertos 8000 y 3000 están libres
- [ ] ✅ No hay procesos de Reflex corriendo
- [ ] ✅ El archivo `rxconfig.py` existe en tu carpeta actual

### 🔍 Verificación Rápida

```bash
# Verificar carpeta y archivos
pwd  # Debe mostrar: /home/felipe/Escritorio/Proyectos/saltoestudia
ls rxconfig.py  # Debe existir

# Verificar puertos
lsof -i :8000 -i :3000 || echo "Puertos libres"

# Si todo está bien, arrancar
reflex run --backend-host 0.0.0.0 --backend-port 8000 --frontend-port 3000
```

### 📝 Notas Importantes

- **No uses** `python3 -m http.server` para servir la app, solo Reflex
- **Siempre ejecuta** Reflex desde la carpeta donde está `rxconfig.py`
- **Si ves errores**, revisa los logs de la terminal
- **Si el puerto está ocupado**, usa el script de limpieza
- **El script funciona** en cualquier VPS con Linux (Ubuntu, Debian, CentOS, etc.)

### 🛠️ Script de Limpieza Detallado

El script `./scripts/limpiar_puertos.sh` incluye:

- **Detección automática** de procesos en puertos 8000 y 3000
- **Información detallada** de qué procesos encontró
- **Confirmación interactiva** antes de matar procesos
- **Verificación final** de que los puertos quedaron libres
- **Instalación automática** de `lsof` si no está disponible
- **Compatibilidad** con diferentes distribuciones Linux
- **Manejo de errores** y mensajes informativos con colores

## 🚀 Arranque rápido para desarrollo local

Si quieres probar el proyecto en tu máquina, simplemente ejecuta:

```bash
./scripts/arrancar_dev.sh
```

Este script:
- Mata procesos que usen los puertos 3000 y 8000
- Se asegura de que la base de datos correcta esté configurada
- Ejecuta migraciones si es necesario
- **Puebla automáticamente la base de datos con datos de prueba si está vacía**
- Arranca Reflex en modo desarrollo

¡Listo! Accede a http://localhost:3000 para ver la app funcionando con datos reales.

## 🚀 Desarrollo

### Ejecutar la aplicación

**Opción 1: Script automático (recomendado)**
```bash
# Libera automáticamente puertos 3000 y 8000 antes de ejecutar
./scripts/reflex-clean.sh
```

**Opción 2: Con npm**
```bash
npm run dev-clean
```

**Opción 3: Manual (puede dar errores de puertos ocupados)**
```bash
reflex run
```

### ¿Por qué usar el script automático?

El script `reflex-clean.sh` resuelve automáticamente el problema común de puertos ocupados:
- Libera el puerto 3000 (frontend) si está ocupado
- Libera el puerto 8000 (backend) si está ocupado
- Ejecuta `reflex run` sin errores
- Funciona en Linux, macOS y Windows (WSL)
