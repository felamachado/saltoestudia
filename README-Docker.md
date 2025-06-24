# Docker Setup - Salto Estudia

## 🔄 Migración Completada: Docker Compose → Dockerfile único

### ¿Qué cambió?

**Antes (Complejo):**
- `docker-compose.yml` + `dockerfile` + `start.sh`
- Múltiples archivos de configuración
- Lógica distribuida entre archivos

**Ahora (Simplificado):**
- ✅ **Un solo `dockerfile`** con toda la configuración
- ✅ **Scripts simples**: `run-dev.sh` y `run-prod.sh`
- ✅ **Misma funcionalidad** pero más mantenible

---

## 🚀 Uso Rápido

### Desarrollo (con hot-reload):
```bash
./run-dev.sh
```

### Producción (sin hot-reload):
```bash
./run-prod.sh
```

### Acceso:
- **Frontend:** http://localhost:3000
- **Backend:** http://localhost:8000

---

## 📋 Comandos Docker Manuales

### Construir imagen:
```bash
docker build -t saltoestudia .
```

### Desarrollo (con volúmenes para hot-reload):
```bash
docker run -d \
  --name saltoestudia-app \
  -p 3000:3000 \
  -p 8000:8000 \
  -v "$(pwd)":/app \
  -v "$(pwd)/data":/app/data \
  saltoestudia
```

### Producción (sin volúmenes):
```bash
docker run -d \
  --name saltoestudia-app \
  -p 3000:3000 \
  -p 8000:8000 \
  saltoestudia
```

---

## 🔧 Gestión del Contenedor

### Ver logs:
```bash
docker logs -f saltoestudia-app
```

### Detener:
```bash
docker stop saltoestudia-app
```

### Eliminar:
```bash
docker rm saltoestudia-app
```

### Estado:
```bash
docker ps
```

---

## 📂 Estructura Simplificada

```
saltoestudia/
├── dockerfile          # ← TODO EN UNO: build + deps + init + run
├── init_db.py          # ← Script de inicialización de BD
├── run-dev.sh          # ← Desarrollo con hot-reload
├── run-prod.sh         # ← Producción optimizada
└── (archivos obsoletos eliminados)
```

---

## ✅ Ventajas del Nuevo Sistema

- **Simplicidad**: Un solo archivo de configuración
- **Consistencia**: Mismo comportamiento en dev y prod
- **Mantenabilidad**: Menos archivos que actualizar
- **Transparencia**: Cambio 100% compatible con setup anterior

---

## 🔄 Hot-reload

El hot-reload **funciona automáticamente** cuando usas `./run-dev.sh`:
- Editas código → Cambios se aplican inmediatamente
- No necesitas reiniciar el contenedor
- Los volúmenes Docker mantienen sincronización

---

## 🎯 Migración Completada

Este sistema **reemplaza completamente**:
- ❌ `docker-compose.yml` (eliminado)
- ❌ `start.sh` (eliminado)  
- ❌ `dockerfile` viejo (backup en `dockerfile.old`)

**¡Mismo resultado, menos complejidad!** 🎉 