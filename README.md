# 🎓 Salto Estudia

Plataforma educativa para la gestión de cursos e instituciones educativas en Salto, Uruguay.

## 🚀 Inicio Rápido

### Opción 1: Script Automático (Recomendado)

```bash
# Configurar entorno de desarrollo
./scripts/setup-env.sh desarrollo

# Iniciar en modo Docker (recomendado)
./scripts/start-project.sh docker

# O iniciar en modo local
./scripts/start-project.sh local

# Ver ayuda
./scripts/start-project.sh help
```

### Opción 2: Manual

```bash
# Clonar el repositorio
git clone <url-del-repositorio>
cd saltoestudia

# Iniciar la aplicación con Docker
docker compose -f docker-compose.desarrollo.yml up -d --build
```

## 🌐 Acceso a la Aplicación

Una vez iniciada, la aplicación estará disponible en:

- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:8000
- **Admin**: http://localhost:3000/admin

## 📚 Páginas Disponibles

- **🏠 Inicio**: Información general del proyecto
- **📖 Cursos**: Buscador de cursos con filtros avanzados
- **🏢 Instituciones**: Galería de instituciones educativas
- **🔐 Admin**: Panel de administración (requiere login)

## 📖 Documentación

- **`DOCUMENTATION.md`** - Índice completo de toda la documentación
- **`README.md`** - Esta guía de inicio rápido
- **`ARCHITECTURE.md`** - Arquitectura completa del sistema
- **`COMPONENTS.md`** - Documentación detallada de componentes
- **`CONFIGURATION.md`** - Configuración del sistema
- **`DATA.md`** - Gestión de datos y migraciones
- **`SCRIPTS.md`** - Scripts de automatización
- **`DEPLOYMENT.md`** - Guía completa de despliegue
- **`DEPLOY-VPS.md`** - Despliegue específico en VPS
- **`ENTORNOS.md`** - Configuración de entornos
- **`DEVELOPMENT-WORKFLOW.md`** - Workflow de desarrollo
- **`TROUBLESHOOTING.md`** - Solución de problemas
- **`SECURITY.md`** - Seguridad del proyecto
- **`CHANGELOG.md`** - Historial de cambios

## 🔧 Configuración Automática

El sistema ahora detecta automáticamente el entorno y configura la base de datos correctamente:

- **Docker**: Usa `/app/data/saltoestudia.db`
- **Local**: Usa `./data/saltoestudia.db`
- **Variable de entorno**: Si `DATABASE_URL` está definida, la usa

No necesitas cambiar configuraciones manualmente.

## 🐳 Docker

### Entornos Disponibles

#### Desarrollo (Local)
```bash
# Configurar entorno de desarrollo
./scripts/setup-env.sh desarrollo

# Iniciar aplicación
docker compose -f docker-compose.desarrollo.yml up -d --build
```

#### Producción (VPS)
```bash
# Configurar entorno de producción
./scripts/setup-env.sh produccion

# Iniciar aplicación
docker compose -f docker-compose.production.yml up -d
```

### Configuración Automática
- **Desarrollo**: Usa `docker-compose.desarrollo.yml` y `config-desarrollo.env`
- **Producción**: Usa `docker-compose.production.yml` y `.env` con contraseñas seguras

### ⚠️ Importante: Solo Docker
Este proyecto se ejecuta **exclusivamente en Docker**. No se puede ejecutar Reflex nativo localmente.

> **📋 Para información detallada sobre archivos necesarios y despliegue, consulta [`DEPLOYMENT.md`](DEPLOYMENT.md)**

## 📊 Base de Datos

La aplicación incluye datos de ejemplo con:
- 6 instituciones educativas
- 10 cursos
- 12 sedes
- Usuarios administradores

## 🔐 Acceso Administrativo

Para acceder al panel de administración:

1. Ve a http://localhost:3000/admin
2. Usa las credenciales configuradas en tu archivo `.env`:
   - Email: `admin@cenur.edu.uy`
   - Contraseña: La configurada en `CENUR_PASSWORD` del archivo `.env`

## 🛠️ Desarrollo

### Estructura del Proyecto

```
saltoestudia/
├── saltoestudia/          # Código principal
│   ├── pages/            # Páginas de la aplicación
│   ├── models.py         # Modelos de base de datos
│   ├── database.py       # Operaciones de BD
│   ├── state.py          # Estado global
│   └── theme.py          # Estilos y temas
├── data/                 # Base de datos SQLite
├── scripts/              # Scripts de utilidad
├── docker-compose.yml    # Configuración Docker (producción)
├── docker-compose.desarrollo.yml  # Configuración Docker (desarrollo)
├── config-desarrollo.env # Variables de entorno (desarrollo)
└── .env.example          # Plantilla de variables de entorno
```

### Comandos Útiles

```bash
# Ver logs de Docker
docker logs saltoestudia-dev-app -f

# Detener aplicación
docker compose -f docker-compose.desarrollo.yml down

# Reiniciar aplicación
./scripts/start-project.sh docker

# Limpiar y reconstruir
docker compose -f docker-compose.desarrollo.yml down
docker compose -f docker-compose.desarrollo.yml up -d --build
```

## 🐛 Solución de Problemas

### La aplicación no carga datos

1. Verifica que la base de datos existe en el contenedor:
   ```bash
   docker exec saltoestudia-dev-app ls -la /app/data/saltoestudia.db
   ```

2. Si no existe, recréala:
   ```bash
   docker exec saltoestudia-dev-app python3 init_db.py
   docker exec saltoestudia-dev-app python3 seed.py
   ```

3. Reinicia la aplicación:
   ```bash
   ./scripts/start-project.sh docker
   ```

### Error de permisos en Docker

```bash
docker exec saltoestudia-dev-app chmod 666 /app/data/saltoestudia.db
docker compose -f docker-compose.desarrollo.yml restart
```

### Puerto ocupado

```bash
# Limpiar puertos
lsof -ti :3000 | xargs -r kill -9
lsof -ti :8000 | xargs -r kill -9
```

## 📝 Notas Importantes

- **Hot Reload**: Los cambios en el código se aplican automáticamente
- **Base de Datos**: Los datos persisten entre reinicios
- **SSL**: En producción se configura automáticamente con Let's Encrypt
- **Logs**: Usa `docker logs saltoestudia-dev-app -f` para ver logs en tiempo real
- **Docker Only**: El proyecto se ejecuta exclusivamente en contenedores Docker

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.
# Test workflow - jue 17 jul 2025 09:24:23 -03
