# 🎓 Salto Estudia

Sistema de gestión de cursos e instituciones educativas de Salto, Uruguay.

Desarrollado con **Reflex** (Python) + **SQLite** + **Docker**, incluye gestión completa de cursos, instituciones y panel administrativo con autenticación.

## ✨ Características

- 🎯 **Buscador de cursos** con filtros avanzados
- 🏛️ **Gestión de instituciones** educativas
- 👨‍💼 **Panel administrativo** por institución
- 🔒 **Autenticación segura** con bcrypt
- 📱 **Diseño responsive** con AG Grid
- 🗄️ **Base de datos SQLite** (sin dependencias externas)
- 🐳 **Docker optimizado** con hot-reload

## 🚀 Inicio Rápido

### Prerrequisitos
- Docker instalado
- Git

### 🔧 Desarrollo (Hot-reload)

```bash
# 1. Clonar el repositorio
git clone https://github.com/felamachado/saltoestudia.git
cd saltoestudia

# 2. Ejecutar en modo desarrollo
./run-dev.sh
```

**¡Listo!** La aplicación estará disponible en:
- **Frontend:** http://localhost:3000
- **Backend:** http://localhost:8000
- **Admin:** http://localhost:3000/admin

### 🏭 Producción

```bash
# Ejecutar en modo producción
./run-prod.sh
```

## 🏗️ Arquitectura

### 📂 Estructura del Proyecto

```
saltoestudia/
├── saltoestudia/           # 🐍 Código fuente principal
│   ├── pages/              # 📄 Páginas de la aplicación
│   │   ├── index.py        # 🏠 Página principal
│   │   ├── cursos.py       # 🎓 Buscador de cursos
│   │   ├── instituciones.py # 🏛️ Galería de instituciones
│   │   ├── admin.py        # 👨‍💼 Panel administrativo
│   │   └── login.py        # 🔐 Autenticación
│   ├── models.py           # 🗄️ Modelos de base de datos
│   ├── database.py         # 🔌 Operaciones CRUD
│   ├── state.py            # 📊 Estado global de Reflex
│   ├── layout.py           # 🎨 Layout y navegación
│   └── theme.py            # 🎨 Sistema de diseño centralizado
├── assets/                 # 🖼️ Recursos estáticos (logos, etc)
├── data/                   # 📁 Base de datos SQLite
├── scripts/                # 🔧 Scripts de utilidad
├── alembic/                # 🔄 Migraciones de base de datos
├── dockerfile              # 🐳 Imagen Docker unificada
├── run-dev.sh              # 🛠️ Script desarrollo (hot-reload)
├── run-prod.sh             # 🏭 Script producción
├── init_db.py              # 🗄️ Inicialización de tablas
├── seed.py                 # 🌱 Datos iniciales
└── requirements.txt        # 📦 Dependencias Python
```

### 🐳 Docker Simplificado

El proyecto usa un **dockerfile unificado** que reemplaza docker-compose + start.sh:

- **`dockerfile`** - Imagen única para desarrollo y producción
- **`run-dev.sh`** - Desarrollo con hot-reload
- **`run-prod.sh`** - Producción optimizada
- **`init_db.py`** - Creación automática de tablas

## 🗄️ Base de Datos

### SQLite (Sin configuración)
- **Archivo:** `./data/saltoestudia.db`
- **Inicialización:** Automática al primer arranque
- **Datos de ejemplo:** Se cargan automáticamente
- **Respaldos:** Simples archivos `.db`

### Respaldos
```bash
# Crear respaldo
cp data/saltoestudia.db backup_$(date +%Y%m%d_%H%M%S).db

# Restaurar desde respaldo
cp backup_20241223_120000.db data/saltoestudia.db
```

## 🛠️ Desarrollo

### Comandos Principales

```bash
# 🏃‍♂️ Desarrollo (hot-reload)
./run-dev.sh

# 🏭 Producción
./run-prod.sh

# 📋 Ver logs en vivo
docker logs -f saltoestudia-dev    # desarrollo
docker logs -f saltoestudia-prod   # producción

# 🔄 Reiniciar contenedor
docker restart saltoestudia-dev

# 🛑 Parar aplicación
docker stop saltoestudia-dev
docker rm saltoestudia-dev
```

### Hot-reload Automático

El modo desarrollo incluye **hot-reload** automático:
- ✅ Cambios en Python se aplican instantáneamente
- ✅ No necesitas reiniciar Docker para cambios de frontend
- ✅ Solo reinicia para cambios en dependencias

### Migraciones de Base de Datos

```bash
# Entrar al contenedor
docker exec -it saltoestudia-dev bash

# Generar nueva migración
alembic revision --autogenerate -m "Descripción del cambio"

# Aplicar migraciones
alembic upgrade head

# Ver historial
alembic history
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

### Lista de Verificación

- [ ] ✅ Cambiar contraseñas por defecto (crear `.env`)
- [ ] ✅ Configurar HTTPS (nginx/traefik)
- [ ] ✅ Configurar respaldos automáticos de SQLite
- [ ] ✅ Monitorear logs con `docker logs -f`
- [ ] ✅ Actualizar dependencias regularmente

### Ejemplo Producción

```bash
# 1. Clonar en servidor
git clone https://github.com/felamachado/saltoestudia.git
cd saltoestudia

# 2. Configurar contraseñas (opcional)
echo 'DEFAULT_SEED_PASSWORD=contraseña_super_segura_2024' > .env

# 3. Ejecutar en producción
./run-prod.sh

# 4. Configurar proxy reverso (nginx)
# server {
#     listen 80;
#     server_name tu-dominio.com;
#     location / {
#         proxy_pass http://localhost:3000;
#     }
# }
```

## 🐛 Solución de Problemas

### Problemas Comunes

**Contenedor no arranca:**
```bash
# Ver logs detallados
docker logs saltoestudia-dev

# Verificar puertos ocupados
lsof -i :3000
lsof -i :8000
```

**Base de datos corrupta:**
```bash
# Eliminar y recrear
rm data/saltoestudia.db
./run-dev.sh  # Se recrea automáticamente
```

**Cambios no se reflejan:**
```bash
# Reflex tiene hot-reload, pero para dependencias:
docker restart saltoestudia-dev
```

**Problemas de permisos:**
```bash
# Cambiar propietario
sudo chown -R $USER:$USER data/
```

## 📊 Datos de Ejemplo

El proyecto incluye datos de ejemplo para Salto, Uruguay:

### 🏛️ Instituciones
- UDELAR – CENUR LN
- IAE Salto  
- Esc. Catalina H. de Castaños
- Esc. De Administración
- Esc. Agraria

### 👥 Usuarios Administradores
- **Emails:** `cenur@cenur.com`, `iae@iae.com`, etc.
- **Contraseña por defecto:** `CHANGE_THIS_PASSWORD_NOW`

### 🎓 Cursos de Ejemplo
- Licenciatura en Informática
- Gestión de Emprendimientos
- Marketing Digital
- Electricidad Domiciliaria
- Y más...

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
- **Ubicación:** Salto, Uruguay
- **Año:** 2024

---

## 🎯 Tecnologías

- **Backend:** Python + Reflex + SQLAlchemy
- **Frontend:** React (generado por Reflex)
- **Base de Datos:** SQLite
- **Containerización:** Docker
- **UI Components:** AG Grid + Chakra UI
- **Autenticación:** bcrypt + sesiones

**⚡ ¡Listo para producción en segundos!** 🚀 