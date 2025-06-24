# 🎓 Salto Estudia

Sistema de gestión de cursos e instituciones educativas de Salto, Uruguay.

## 🚀 Inicio Rápido

### Prerrequisitos
- Docker y Docker Compose instalados
- Git

### 🔧 Configuración Inicial

1. **Clonar el repositorio:**
```bash
git clone <url-del-repositorio>
cd saltoestudia
```

2. **Configurar variables de entorno:**
```bash
# Copiar la plantilla de configuración
cp .env.example .env

# Editar el archivo .env con tus credenciales seguras
nano .env  # o usar tu editor preferido
```

3. **Generar contraseñas seguras:**
```bash
# Para generar contraseñas aleatorias seguras:
openssl rand -base64 32
```

4. **Construir y ejecutar los contenedores:**
```bash
# Construir e iniciar todos los servicios
docker-compose up --build

# O en modo background:
docker-compose up --build -d
```

5. **La base de datos se inicializa automáticamente:**
```bash
# Los datos se poblarán automáticamente al iniciar
# No se requiere configuración adicional
```

## 🌐 Acceso a la Aplicación

- **Aplicación principal:** http://localhost:3000
- **Panel de administración:** http://localhost:3000/admin

## 🏗️ Arquitectura

### Servicios Docker

- **`app`** - Aplicación principal (Frontend + Backend)
  - Puerto 3000: Frontend (React)
  - Puerto 8000: Backend (FastAPI)
  - Base de datos: SQLite (archivo local)

### Estructura del Proyecto

```
saltoestudia/
├── saltoestudia/           # Código fuente principal
│   ├── pages/              # Páginas de la aplicación
│   ├── models.py           # Modelos de base de datos
│   ├── state.py            # Estado global de Reflex
│   └── theme.py            # Sistema de diseño centralizado
├── assets/                 # Recursos estáticos
├── alembic/                # Migraciones de base de datos
├── docker-compose.yml      # Configuración de Docker
├── dockerfile              # Imagen de la aplicación
└── .env.example            # Plantilla de variables de entorno
```

## 🔐 Seguridad

### Variables de Entorno

**IMPORTANTE:** Nunca subas el archivo `.env` a GitHub. Siempre usa `.env.example` como plantilla.

```bash
# ✅ Correcto - archivo versionado
.env.example

# ❌ NUNCA hacer - contiene secretos
.env
```

### Contraseñas Recomendadas

- **Mínimo 16 caracteres**
- **Combinar letras, números y símbolos**
- **Evitar palabras comunes o predecibles**
- **Cambiar regularmente en producción**

### Generar Contraseñas Seguras

```bash
# Generar contraseña de 32 caracteres
openssl rand -base64 32

# Generar múltiples opciones
for i in {1..5}; do openssl rand -base64 32; done
```

## 🛠️ Desarrollo

### Comandos Útiles

```bash
# Ver logs de todos los servicios
docker-compose logs -f

# Ver logs de un servicio específico
docker-compose logs -f reflex

# Reiniciar un servicio
docker-compose restart reflex

# Acceder al contenedor de la aplicación
docker-compose exec reflex bash

# Parar todos los servicios
docker-compose down

# Parar todos los servicios
docker-compose down

# Parar y eliminar volúmenes (¡cuidado con los datos de SQLite!)
docker-compose down -v
```

### Base de Datos

```bash
# La base de datos SQLite se encuentra en ./data/saltoestudia.db
# No requiere configuración adicional

# Crear respaldo de la base de datos
cp data/saltoestudia.db backup_$(date +%Y%m%d_%H%M%S).db

# Restaurar desde respaldo
cp backup_YYYYMMDD_HHMMSS.db data/saltoestudia.db
```

### Migraciones

```bash
# Generar nueva migración
docker-compose exec app alembic revision --autogenerate -m "Descripción del cambio"

# Aplicar migraciones
docker-compose exec app alembic upgrade head

# Ver historial de migraciones
docker-compose exec app alembic history
```

## 📦 Despliegue en Producción

### Lista de Verificación de Seguridad

- [ ] Cambiar todas las contraseñas por defecto
- [ ] Usar contraseñas seguras (mínimo 16 caracteres)
- [ ] Configurar HTTPS
- [ ] Proteger el archivo de base de datos SQLite
- [ ] Configurar respaldos automáticos
- [ ] Actualizar dependencias regularmente

### Variables de Producción

```bash
# Ejemplo de .env para producción
DATABASE_URL=sqlite:///data/saltoestudia.db
DEFAULT_SEED_PASSWORD=contraseña_super_segura_2024
ENVIRONMENT=production
```

## 🐛 Solución de Problemas

### Problemas Comunes

**Error de conexión a la base de datos:**
```bash
# Verificar que los contenedores estén ejecutándose
docker-compose ps

# Verificar logs de la aplicación
docker-compose logs app

# Verificar que el archivo de base de datos existe
ls -la data/saltoestudia.db
```

**Cambios no se reflejan:**
```bash
# Reflex tiene hot-reload, pero a veces necesitas:
docker-compose restart app

# O reconstruir completamente:
docker-compose up --build
```

**Problemas de permisos:**
```bash
# Cambiar propietario de archivos
sudo chown -R $USER:$USER .
```

## 🤝 Contribuir

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 📞 Contacto

- **Proyecto:** Salto Estudia
- **Ubicación:** Salto, Uruguay
- **Año:** 2024

---

**⚠️ Recordatorio de Seguridad:** Siempre revisa que el archivo `.env` esté en `.gitignore` antes de hacer commit. ¡Nunca subas credenciales a GitHub! 