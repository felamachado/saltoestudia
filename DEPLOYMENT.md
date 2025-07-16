# 🚀 Guía de Despliegue - Salto Estudia

Esta guía explica cómo desplegar el proyecto Salto Estudia en diferentes entornos y qué archivos son necesarios para que funcione correctamente.

## 📋 Resumen de Entornos

| Entorno | Rama Git | Dominio | Contenedor | Configuración |
|---------|----------|---------|------------|---------------|
| **Desarrollo** | `desarrollo` | `desarrollo.saltoestudia.infra.com.uy` | `saltoestudia-dev-app` | `docker-compose.desarrollo.yml` |
| **Producción** | `main` | `saltoestudia.infra.com.uy` | `saltoestudia-app` | `docker-compose.yml` |

## 🐳 Despliegue Dockerizado

### **Desarrollo Local**
```bash
# 1. Configurar entorno de desarrollo
./scripts/setup-env.sh desarrollo

# 2. Iniciar aplicación
docker compose up -d

# 3. Verificar funcionamiento
docker compose logs -f
```

### **Producción (VPS)**
```bash
# 1. Configurar entorno de producción
./scripts/setup-env.sh produccion

# 2. Iniciar aplicación
docker compose up -d

# 3. Verificar funcionamiento
docker compose logs -f
```

## 📁 Archivos Necesarios para Producción

### **Archivos que SÍ van a GitHub (Código)**
- ✅ Todo el código fuente (`saltoestudia/`)
- ✅ Configuración Docker (`docker-compose.yml`, `dockerfile.production`)
- ✅ Dependencias (`requirements.txt`, `package.json`)
- ✅ Scripts de utilidad (`scripts/`)
- ✅ Documentación (`README.md`, `ENTORNOS.md`, etc.)
- ✅ Plantillas de configuración (`.env.example`, `config-desarrollo.env`)

### **Archivos que NO van a GitHub pero SÍ necesitas en producción**

#### **1. Archivo de Variables de Entorno (CRÍTICO)**
```bash
# Archivo: .env
# Ubicación en VPS: /srv/docker/saltoestudia/.env
```

**Contenido necesario:**
```bash
# === BASE DE DATOS ===
DATABASE_URL=sqlite:///data/saltoestudia.db
REFLEX_DB_URL=sqlite:///reflex.db

# === CONTRASEÑAS SEGURAS PARA PRODUCCIÓN ===
# IMPORTANTE: NO usar las contraseñas de desarrollo
DEFAULT_SEED_PASSWORD=tu_contraseña_segura_aqui
CENUR_PASSWORD=contraseña_cenur_segura
IAE_PASSWORD=contraseña_iae_segura
CATALINA_PASSWORD=contraseña_catalina_segura
ADMINISTRACION_PASSWORD=contraseña_admin_segura
AGRARIA_PASSWORD=contraseña_agraria_segura

# === CONFIGURACIÓN DE PRODUCCIÓN ===
REFLEX_ENV=production
DEBUG=false
```

#### **2. Base de Datos (opcional)**
```bash
# Archivo: data/saltoestudia.db
# Ubicación en VPS: /srv/docker/saltoestudia/data/saltoestudia.db
# Solo si quieres migrar datos existentes desde desarrollo
```

#### **3. Logs (opcional)**
```bash
# Directorio: logs/
# Ubicación en VPS: /srv/docker/saltoestudia/logs/
# Solo si quieres preservar logs existentes
```

## 🔄 Cómo Copiar Archivos al VPS

### **Opción 1: Manual (Recomendado para primera vez)**

```bash
# 1. Copiar archivo .env al VPS
scp .env ubuntu@150.230.30.198:/srv/docker/saltoestudia/

# 2. Copiar base de datos (si la tienes y quieres migrar)
scp data/saltoestudia.db ubuntu@150.230.30.198:/srv/docker/saltoestudia/data/

# 3. Copiar logs (opcional)
scp -r logs/ ubuntu@150.230.30.198:/srv/docker/saltoestudia/
```

### **Opción 2: Usar el script de deploy**

```bash
# El script deploy-to-vps.sh ya incluye la copia de .env y data/
./deploy-to-vps.sh
```

### **Opción 3: Crear .env directamente en el VPS**

```bash
# 1. Conectarte al VPS
ssh ubuntu@150.230.30.198

# 2. Ir al directorio del proyecto
cd /srv/docker/saltoestudia

# 3. Crear .env con contraseñas seguras
nano .env

# 4. Configurar permisos
chmod 600 .env
```

## 🔐 Seguridad - Archivos Críticos

### **NUNCA subir a GitHub:**
- ❌ `.env` (contiene contraseñas reales)
- ❌ `data/saltoestudia.db` (contiene datos reales)
- ❌ `logs/` (puede contener información sensible)
- ❌ Cualquier archivo con credenciales reales

### **SÍ subir a GitHub:**
- ✅ `.env.example` (plantilla sin contraseñas reales)
- ✅ `config-desarrollo.env` (solo contraseñas de desarrollo)
- ✅ Todo el código fuente
- ✅ Configuración Docker
- ✅ Scripts de utilidad

## 🔧 Verificación en el VPS

### **Después de copiar los archivos:**

```bash
# 1. Conectarte al VPS
ssh ubuntu@150.230.30.198

# 2. Verificar archivos
cd /srv/docker/saltoestudia
ls -la .env data/saltoestudia.db

# 3. Verificar permisos
chmod 600 .env
chmod 644 data/saltoestudia.db

# 4. Verificar configuración
./scripts/verify-production-setup.sh

# 5. Iniciar aplicación
docker compose up -d

# 6. Verificar logs
docker compose logs -f
```

## 🔄 GitHub Actions (Deploy Automático)

### **Desarrollo:**
- **Trigger:** Push a rama `desarrollo`
- **Workflow:** `.github/workflows/deploy-desarrollo.yml`
- **Acciones:**
  1. Copia `docker-compose.desarrollo.yml` → `docker-compose.yml`
  2. Copia `config-desarrollo.env` → `.env`
  3. Despliega en `/srv/docker/saltoestudia-desarrollo/`

### **Producción:**
- **Trigger:** Push a rama `main`
- **Workflow:** `.github/workflows/deploy-produccion.yml`
- **Acciones:**
  1. Usa `docker-compose.yml` original
  2. Usa `.env` con contraseñas de producción (debe existir en VPS)
  3. Despliega en `/srv/docker/saltoestudia/`

## 📋 Checklist para Despliegue de Producción

### **Antes del Deploy:**
- [ ] **`.env`** configurado con contraseñas seguras (NO las de desarrollo)
- [ ] **`data/saltoestudia.db`** copiada (si quieres migrar datos)
- [ ] **Permisos correctos** (600 para .env, 644 para .db)
- [ ] **Configuración de producción** (REFLEX_ENV=production)
- [ ] **Verificación local** ejecutada (`./scripts/verify-production-setup.sh`)

### **Durante el Deploy:**
- [ ] **Push a rama `main`** para trigger automático
- [ ] **Verificar logs** del workflow en GitHub Actions
- [ ] **Verificar logs** del contenedor en VPS

### **Después del Deploy:**
- [ ] **Verificar aplicación** en `https://saltoestudia.infra.com.uy`
- [ ] **Verificar autenticación** con credenciales de producción
- [ ] **Verificar funcionalidad** completa (cursos, instituciones, admin)

## 🚨 Troubleshooting

### **Problema: Contenedor no inicia**
```bash
# Verificar configuración
docker compose config

# Ver logs
docker compose logs

# Verificar archivo .env
cat .env
```

### **Problema: Error de autenticación**
```bash
# Verificar que .env tiene contraseñas correctas
grep -E "(CENUR_PASSWORD|IAE_PASSWORD)" .env

# Verificar que no son contraseñas de desarrollo
grep "dev_password_123" .env
```

### **Problema: Dominio no funciona**
```bash
# Verificar contenedor está corriendo
docker ps | grep saltoestudia-app

# Verificar red Traefik
docker network inspect traefik-net | grep saltoestudia-app

# Verificar logs de Traefik
docker logs traefik
```

### **Problema: Base de datos no funciona**
```bash
# Verificar archivo de base de datos
ls -la data/saltoestudia.db

# Verificar permisos
chmod 644 data/saltoestudia.db

# Verificar conectividad
docker exec saltoestudia-app ls -la /app/data/
```

## 📞 Contacto y Soporte

Si tienes problemas con el despliegue:

1. **Revisa los logs:** `docker compose logs -f`
2. **Verifica la configuración:** `./scripts/verify-production-setup.sh`
3. **Consulta la documentación:** `ENTORNOS.md`, `TROUBLESHOOTING.md`
4. **Revisa GitHub Actions:** Para ver logs del deploy automático

---

**Nota importante:** El archivo `.env` con las contraseñas reales es el más crítico. Sin él, la aplicación no podrá autenticarse correctamente en producción. Asegúrate de que esté configurado antes de hacer el deploy. 