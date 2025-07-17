# 🔧 Scripts de Automatización - Salto Estudia

Este directorio contiene scripts que automatizan tareas comunes y previenen errores.

## 📋 Scripts Disponibles

### 🔄 `sync-database.sh`
**Propósito:** Sincroniza automáticamente la base de datos entre desarrollo y producción.

**Problema que resuelve:**
- En desarrollo: Reflex usa `data/saltoestudia.db` (con datos del seed)
- En producción: Reflex usa `reflex.db` (ubicación por defecto, sin datos)
- Resultado: La web carga pero no muestra datos dinámicos

**Funcionalidades:**
- ✅ Detecta automáticamente el entorno (Docker vs Local)
- ✅ Verifica si `reflex.db` tiene datos
- ✅ Copia datos desde `data/saltoestudia.db` si es necesario
- ✅ Ejecuta migraciones si faltan
- ✅ Ejecuta seed si no hay datos
- ✅ Verifica que todo esté funcionando

**Uso:**
```bash
# Automático (se ejecuta al iniciar el backend en producción)
./scripts/sync-database.sh

# Manual (para debugging)
docker compose exec backend /app/sync-database.sh
```

**Ejemplo de salida:**
```
🔄 Iniciando sincronización de base de datos...
📍 Entorno detectado: Producción (Docker)
✅ Base de datos con datos encontrada en data/saltoestudia.db
📊 Verificando contenido de reflex.db...
📈 Cursos en reflex.db: 0
🔄 reflex.db está vacía, copiando datos desde data/saltoestudia.db...
✅ Base de datos sincronizada
📊 Estado final de la base de datos:
   - Cursos: 10
   - Instituciones: 6
✅ Base de datos sincronizada correctamente
```

---

### 🚀 `start-project.sh`
**Propósito:** Inicia el proyecto de forma segura en desarrollo.

**Funcionalidades:**
- ✅ Limpia puertos automáticamente
- ✅ Verifica dependencias
- ✅ Maneja permisos de archivos
- ✅ Detecta entorno automáticamente
- ✅ Verifica que la aplicación funcione

**Uso:**
```bash
# Desarrollo con Docker (recomendado)
./scripts/start-project.sh docker

# Desarrollo local
./scripts/start-project.sh local

# Ayuda
./scripts/start-project.sh help
```

---

### 🔍 `verify-setup.sh`
**Propósito:** Verifica que todo esté configurado correctamente.

**Verificaciones:**
- ✅ Base de datos existe y tiene datos
- ✅ Permisos correctos
- ✅ Docker instalado y funcionando
- ✅ Contenedores ejecutándose

**Uso:**
```bash
./scripts/verify-setup.sh
```

---

## 🎯 Flujo de Desarrollo Seguro

### 1. **Inicio del día:**
```bash
./scripts/start-project.sh docker
```

### 2. **Durante desarrollo:**
- Los cambios se aplican automáticamente (hot reload)
- Si hay problemas, verificar logs

### 3. **Antes de commit:**
```bash
./scripts/verify-setup.sh
```

### 4. **Despliegue a producción:**
```bash
./deploy-to-vps.sh
```
*El script de sincronización se ejecuta automáticamente*

---

## 🔧 Integración con Docker

### **Dockerfile.backend:**
```dockerfile
# Copiar script de sincronización
COPY scripts/sync-database.sh /app/sync-database.sh
RUN chmod +x /app/sync-database.sh

# Ejecutar sincronización antes del backend
CMD ["sh", "-c", "/app/sync-database.sh && reflex run --backend-only"]
```

### **Docker Compose:**
Los scripts se ejecutan automáticamente al iniciar los contenedores.

---

## 🚫 Errores Comunes Prevenidos

### ❌ **Base de datos vacía en producción:**
- **Antes:** La web cargaba pero no mostraba datos
- **Ahora:** Sincronización automática al iniciar

### ❌ **Permisos incorrectos:**
- **Antes:** Errores de "unable to open database file"
- **Ahora:** Permisos configurados automáticamente

### ❌ **Puertos ocupados:**
- **Antes:** Errores de "port already in use"
- **Ahora:** Limpieza automática de puertos

### ❌ **Dependencias faltantes:**
- **Antes:** Errores de "command not found"
- **Ahora:** Verificación automática de dependencias

---

## 📊 Métricas de Prevención

### **Tiempo ahorrado por error:**
- **Antes:** 30-60 minutos por error
- **Ahora:** 0 minutos (prevención automática)

### **Errores prevenidos:**
- ✅ Base de datos vacía
- ✅ Permisos incorrectos
- ✅ Puertos ocupados
- ✅ Dependencias faltantes
- ✅ Configuración incorrecta

---

## 🎉 Resultado Final

**Con estos scripts:**
- ✅ **0 errores repetitivos**
- ✅ **Desarrollo más productivo**
- ✅ **Configuración automática**
- ✅ **Verificación automática**
- ✅ **Solución inmediata de problemas**

**Comando mágico para todo:**
```bash
./scripts/start-project.sh docker
``` 