# 🌍 Entornos de Salto Estudia

Este documento describe la configuración y separación entre los entornos de desarrollo y producción.

## 📋 Resumen de Entornos

| Aspecto | Desarrollo | Producción |
|---------|------------|------------|
| **Dominio** | `desarrollo.saltoestudia.infra.com.uy` | `saltoestudia.infra.com.uy` |
| **Contenedor** | `saltoestudia-dev-app` | `saltoestudia-app` |
| **Configuración** | `docker-compose.desarrollo.yml` | `docker-compose.yml` |
| **Variables** | `config-desarrollo.env` | `.env` (con contraseñas seguras) |
| **Rama Git** | `desarrollo` | `main` |
| **GitHub Actions** | `deploy-desarrollo.yml` | `deploy-produccion.yml` |

## 🚀 Configuración Rápida

### Desarrollo Local
```bash
# Configurar entorno de desarrollo
./scripts/setup-env.sh desarrollo

# Iniciar aplicación
docker compose up -d
```

### Producción (VPS)
```bash
# Configurar entorno de producción
./scripts/setup-env.sh produccion

# Iniciar aplicación
docker compose up -d
```

## 🔧 Configuración Detallada

### Archivos de Configuración

#### Desarrollo
- **`docker-compose.desarrollo.yml`**: Configuración Docker para desarrollo
  - Contenedor: `saltoestudia-dev-app`
  - Dominio: `desarrollo.saltoestudia.infra.com.uy`
  - Labels Traefik: `saltoestudia-dev-frontend`, `saltoestudia-dev-backend`

- **`config-desarrollo.env`**: Variables de entorno para desarrollo
  - Contraseñas de desarrollo (NO usar en producción)
  - `REFLEX_ENV=development`
  - `DEBUG=true`

#### Producción
- **`docker-compose.yml`**: Configuración Docker para producción
  - Contenedor: `saltoestudia-app`
  - Dominio: `saltoestudia.infra.com.uy`
  - Labels Traefik: `saltoestudia-frontend`, `saltoestudia-backend`

- **`.env`**: Variables de entorno para producción
  - Contraseñas seguras reales
  - `REFLEX_ENV=production`
  - `DEBUG=false`

## 🔄 GitHub Actions

### Workflow de Desarrollo
- **Archivo**: `.github/workflows/deploy-desarrollo.yml`
- **Trigger**: Push a rama `desarrollo`
- **Acciones**:
  1. Copia `docker-compose.desarrollo.yml` → `docker-compose.yml`
  2. Copia `config-desarrollo.env` → `.env`
  3. Despliega en `/srv/docker/saltoestudia-desarrollo/`

### Workflow de Producción
- **Archivo**: `.github/workflows/deploy-produccion.yml`
- **Trigger**: Push a rama `main`
- **Acciones**:
  1. Usa `docker-compose.yml` original
  2. Usa `.env` con contraseñas de producción
  3. Despliega en `/srv/docker/saltoestudia/`

## 🔐 Seguridad

### Desarrollo
- Contraseñas simples para facilitar desarrollo
- Dominio separado para evitar conflictos
- Contenedores con nombres diferenciados

### Producción
- Contraseñas seguras y únicas
- Dominio principal
- Configuración optimizada para rendimiento

## 📊 Monitoreo

### Verificar Entorno Actual
```bash
# Ver configuración actual
docker compose config

# Ver variables de entorno
cat .env | grep -E "(REFLEX_ENV|DEBUG)"

# Ver contenedor activo
docker ps | grep saltoestudia
```

### Logs por Entorno
```bash
# Desarrollo
docker logs saltoestudia-dev-app -f

# Producción
docker logs saltoestudia-app -f
```

## 🚨 Notas Importantes

1. **Nunca usar contraseñas de desarrollo en producción**
2. **El archivo `.env` nunca debe subirse a Git**
3. **Los workflows de GitHub Actions manejan automáticamente la configuración**
4. **Siempre verificar el entorno antes de hacer deploy**
5. **Usar el script `setup-env.sh` para cambiar entre entornos**

## 🔧 Troubleshooting

### Problema: Contenedor no inicia
```bash
# Verificar configuración
./scripts/setup-env.sh desarrollo
docker compose config

# Ver logs
docker compose logs
```

### Problema: Dominio no funciona
```bash
# Verificar labels de Traefik
docker compose config | grep traefik

# Verificar red
docker network ls | grep traefik
```

### Problema: Variables de entorno incorrectas
```bash
# Verificar archivo .env
cat .env

# Reconfigurar entorno
./scripts/setup-env.sh desarrollo
``` 