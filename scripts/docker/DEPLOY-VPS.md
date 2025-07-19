# 🚀 Despliegue de Salto Estudia en VPS

## 📋 Estructura de Archivos

### **Desarrollo Local:**
```
saltoestudia/
├── dockerfile                 # ✅ Para desarrollo local
├── docker-compose.yml        # ✅ Para desarrollo local
└── rxconfig.py               # ✅ Configuración local
```

### **Producción VPS:**
```
saltoestudia/
├── dockerfile.production         # 🆕 Optimizado para VPS
├── docker-compose.production.yml # 🆕 Con configuración Traefik
└── deploy-to-vps.sh             # 🆕 Script automatizado
```

---

## 🔧 Diferencias Local vs Producción

| Aspecto | Local | Producción |
|---------|-------|------------|
| **Arquitectura** | 1 contenedor (`reflex run`) | 2 contenedores (frontend + backend) |
| **Dockerfile** | `reflex run` simple | `reflex export` + `http.server` (frontend) / `reflex run --backend-only` (backend) |
| **Base de datos** | `data/saltoestudia.db` | `reflex.db` (sincronizada automáticamente) |
| **Proxy** | Sin proxy | Traefik con rutas separadas |
| **SSL** | HTTP (`ws://`) | HTTPS (`wss://`) |
| **Puertos** | Directo 3000/8000 | Via Traefik 443 |
| **WebSocket** | `localhost:8000/_event` | `saltoestudia.infra.com.uy/_event` |

---

## 🚀 Desplegar a VPS

### **⚠️ CONFIGURACIÓN CRÍTICA DEL ARCHIVO .ENV**

**IMPORTANTE**: Antes de desplegar, asegúrate de que el archivo `.env` en el VPS esté configurado correctamente para PostgreSQL:

```bash
# CONFIGURACIÓN DE ENTORNO - SALTO ESTUDIA (PRODUCCIÓN)
# ========================================

# === BASE DE DATOS POSTGRESQL ===
DATABASE_URL=postgresql://saltoestudia:SaltoEstudia2024_Postgres!@postgres:5432/saltoestudia
REFLEX_DB_URL=postgresql://saltoestudia:SaltoEstudia2024_Postgres!@postgres:5432/saltoestudia
DB_PASSWORD=SaltoEstudia2024_Postgres!

# === CONTRASEÑAS INDIVIDUALES DE USUARIOS ADMINISTRADORES ===
DEFAULT_SEED_PASSWORD=SaltoEstudia2024_Default!
CENUR_PASSWORD=Cenur_Segura_2024!
IAE_PASSWORD=IAE_Admin_2024!
CATALINA_PASSWORD=Catalina_Tech_2024!
ADMINISTRACION_PASSWORD=Admin_Escuela_2024!
AGRARIA_PASSWORD=Agraria_Campo_2024!

# === CONFIGURACIÓN DE PRODUCCIÓN ===
REFLEX_ENV=production
```

**Si el archivo `.env` no está configurado correctamente:**
- PostgreSQL no se inicializará
- Los contenedores se reiniciarán constantemente
- La aplicación no mostrará datos dinámicos

**Para actualizar el .env en el VPS:**
```bash
# Opción 1: Crear archivo local y subirlo
scp env.production ubuntu@150.230.30.198:/srv/docker/saltoestudia/.env

# Opción 2: Editar directamente en el VPS
ssh ubuntu@150.230.30.198
cd /srv/docker/saltoestudia
nano .env
```

### **Método 1: Script Automatizado (Recomendado)**

```bash
# Desde tu directorio local del proyecto:
./deploy-to-vps.sh
```

**El script automáticamente:**
- ✅ Verifica archivos necesarios
- ✅ Hace backup de configuración actual
- ✅ Copia código y configuración
- ✅ Construye imagen de producción
- ✅ Despliega con Traefik
- ✅ Reinicia servicios

### **Método 2: Manual**

```bash
# 1. Copiar archivos al VPS
rsync -av . ubuntu@150.230.30.198:/srv/docker/saltoestudia/
scp dockerfile.production ubuntu@150.230.30.198:/srv/docker/saltoestudia/dockerfile
scp docker-compose.production.yml ubuntu@150.230.30.198:/srv/docker/saltoestudia/docker-compose.yml

# 2. Conectar al VPS
ssh ubuntu@150.230.30.198

# 3. Construir y desplegar
cd /srv/docker/saltoestudia
docker-compose down
docker-compose build --no-cache
docker-compose up -d
docker restart traefik
```

---

## 🌐 Configuración Traefik

### **Frontend (Puerto 3000):**
- Archivos estáticos: `/_next`, `/favicon`, `/logo`, `/`
- HTML, CSS, JavaScript, imágenes

### **Backend (Puerto 8000):**
- WebSocket: `/_event`
- APIs dinámicas
- Todo lo que NO sea archivos estáticos

### **Labels de Traefik:**
```yaml
# Frontend (archivos estáticos)
traefik.http.routers.saltoestudia-frontend.rule=Host(`saltoestudia.infra.com.uy`) && !PathPrefix(`/_event`)

# Backend (WebSocket y APIs)
traefik.http.routers.saltoestudia-backend.rule=Host(`saltoestudia.infra.com.uy`) && PathPrefix(`/_event`)
```

### **Sincronización Automática de Base de Datos:**
El script `scripts/sync-database.sh` se ejecuta automáticamente al iniciar el backend y:
- ✅ Detecta si `reflex.db` está vacía
- ✅ Copia datos desde `data/saltoestudia.db` si es necesario
- ✅ Ejecuta migraciones si faltan
- ✅ Ejecuta seed si no hay datos
- ✅ Verifica que todo esté funcionando

### **🔄 Inicialización Manual de Base de Datos (Si es necesario):**

Si los contenedores están corriendo pero no hay datos, ejecuta manualmente:

```bash
# Conectar al VPS
ssh ubuntu@150.230.30.198

# Ir al directorio del proyecto
cd /srv/docker/saltoestudia

# Ejecutar migraciones
docker compose exec backend reflex db migrate

# Poblar base de datos con datos iniciales
docker compose exec backend python seed.py

# Reiniciar backend para aplicar cambios
docker compose restart backend
```

**Datos que se crean automáticamente:**
- 📚 6 instituciones con sus sedes
- 👥 6 usuarios administradores con contraseñas individuales
- 🏙️ 18 ciudades del Uruguay
- 📖 10 cursos de diferentes categorías

---

## 📊 Verificar Despliegue

### **Estado de Servicios:**
```bash
ssh ubuntu@150.230.30.198 'cd /srv/docker/saltoestudia && docker-compose ps'
```

### **Logs de Aplicación:**
```bash
ssh ubuntu@150.230.30.198 'docker logs saltoestudia-app -f'
```

### **Probar WebSocket:**
```bash
curl -s -I https://saltoestudia.infra.com.uy/_event
# Debería devolver: HTTP/2 307 (redirect para WebSocket upgrade)
```

### **Verificar Frontend:**
```bash
curl -s -I https://saltoestudia.infra.com.uy/
# Debería devolver: HTTP/2 200 con contenido HTML
```

---

## 🔄 Actualizar Aplicación

### **Para cambios de código:**
```bash
./deploy-to-vps.sh
```

### **Solo reiniciar servicios:**
```bash
ssh ubuntu@150.230.30.198 'cd /srv/docker/saltoestudia && docker-compose restart'
```

### **Reconstruir imagen:**
```bash
ssh ubuntu@150.230.30.198 'cd /srv/docker/saltoestudia && docker-compose build --no-cache && docker-compose up -d'
```

---

## 🔧 Troubleshooting

### **WebSocket no conecta:**
- Verificar que Traefik esté funcionando: `docker ps | grep traefik`
- Reiniciar Traefik: `docker restart traefik`
- Verificar labels: `docker inspect saltoestudia-app | grep traefik`

### **Página no carga:**
- Verificar logs: `docker logs saltoestudia-app --tail 20`
- Verificar estado: `docker-compose ps`

### **SSL no funciona:**
- Verificar certificados: `docker logs traefik | grep saltoestudia`
- Puede tomar unos minutos generar certificados

---

## 📝 Notas Importantes

1. **No modificar archivos originales** (`dockerfile`, `docker-compose.yml`) - mantienen compatibilidad local
2. **Variables de entorno** se configuran automáticamente para producción
3. **Base de datos** se sincroniza desde local a VPS
4. **Backup automático** de configuración antes de cada despliegue
5. **Dominio fijo**: `saltoestudia.infra.com.uy` (cambiar en archivos si necesario)

---

## 🎯 Resultado Final

✅ **Frontend**: https://saltoestudia.infra.com.uy/
✅ **Instituciones**: https://saltoestudia.infra.com.uy/instituciones/
✅ **Cursos**: https://saltoestudia.infra.com.uy/cursos/
✅ **WebSocket**: Funcionando automáticamente
✅ **SSL**: Certificados automáticos Let's Encrypt 