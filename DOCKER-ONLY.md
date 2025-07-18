# 🐳 DOCKER ONLY - Salto Estudia

## ⚠️ ADVERTENCIA CRÍTICA

**Este proyecto SOLO se ejecuta en Docker. NO se puede ejecutar Reflex nativo localmente.**

## 🚫 Por qué NO Reflex Nativo

### Problemas Técnicos
1. **Configuración de Base de Datos**: El proyecto está configurado para usar rutas específicas de contenedores (`/app/data/`)
2. **Variables de Entorno**: Las variables están optimizadas para Docker
3. **Dependencias**: Algunas dependencias están configuradas específicamente para contenedores
4. **Conflictos de Puertos**: El proyecto usa puertos específicos que pueden estar ocupados
5. **Rutas de Archivos**: Las rutas están configuradas para el sistema de archivos de Docker

### Errores Comunes al Usar Reflex Nativo
```bash
# ❌ Esto causará errores:
reflex run
reflex run --loglevel debug
reflex run --frontend-only
reflex run --backend-only

# Errores típicos:
# - Database connection failed
# - File not found: /app/data/saltoestudia.db
# - Port already in use
# - Environment variables not found
```

## ✅ Solución Correcta

### Siempre usar Docker:
```bash
# ✅ CORRECTO - Desarrollo
docker compose -f docker-compose.desarrollo.yml up -d

# ✅ CORRECTO - Producción
docker compose -f docker-compose.production.yml up -d

# ✅ CORRECTO - Con rebuild
docker compose -f docker-compose.desarrollo.yml up -d --build
```

## 🔧 Scripts de Inicio

### Script Automático (Recomendado)
```bash
# Configurar entorno
./scripts/setup-env.sh desarrollo

# Iniciar en Docker
./scripts/start-project.sh docker
```

### Comandos Útiles
```bash
# Ver logs
docker logs saltoestudia-dev-frontend -f
docker logs saltoestudia-dev-backend -f

# Detener
docker compose -f docker-compose.desarrollo.yml down

# Reiniciar
docker compose -f docker-compose.desarrollo.yml restart

# Limpiar todo
docker compose -f docker-compose.desarrollo.yml down -v
docker system prune -f
```

## 🐛 Solución de Problemas

### Si intentaste usar Reflex Nativo y hay errores:

1. **Detener procesos de Reflex:**
```bash
pkill -f "reflex run"
pkill -f granian
```

2. **Limpiar puertos:**
```bash
lsof -ti :3000 | xargs -r kill -9
lsof -ti :8000 | xargs -r kill -9
lsof -ti :8001 | xargs -r kill -9
```

3. **Usar Docker correctamente:**
```bash
docker compose -f docker-compose.desarrollo.yml up -d
```

### Verificar que Docker funciona:
```bash
# Verificar contenedores
docker ps

# Verificar logs
docker logs saltoestudia-dev-frontend --tail 10
docker logs saltoestudia-dev-backend --tail 10

# Verificar acceso
curl -I http://localhost:3000
curl -I http://localhost:8000
```

## 📋 Checklist de Inicio

- [ ] Docker está instalado y funcionando
- [ ] Puerto 3000 libre
- [ ] Puerto 8000 libre
- [ ] Puerto 5432 libre (PostgreSQL)
- [ ] Archivo `config-desarrollo.env` existe
- [ ] **NO ejecutar `reflex run` directamente**
- [ ] Usar `docker compose -f docker-compose.desarrollo.yml up -d`

## 🎯 Resumen

**SALTO ESTUDIA = DOCKER ONLY**

- ❌ `reflex run` → NO FUNCIONA
- ✅ `docker compose up` → FUNCIONA PERFECTAMENTE

**Recuerda: Este proyecto fue diseñado específicamente para Docker desde el inicio.** 