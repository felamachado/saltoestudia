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
| **Dockerfile** | `reflex run` simple | `reflex run --backend-host 0.0.0.0 --backend-port 8000 --frontend-port 3000` |
| **Proxy** | Sin proxy | Traefik con rutas separadas |
| **SSL** | HTTP (`ws://`) | HTTPS (`wss://`) |
| **Puertos** | Directo 3000/8000 | Via Traefik 443 |
| **WebSocket** | `localhost:8000/_event` | `saltoestudia.infra.com.uy/_event` |

---

## 🚀 Desplegar a VPS

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
# Frontend
traefik.http.routers.saltoestudia-frontend.rule=Host(`saltoestudia.infra.com.uy`) && (PathPrefix(`/_next`) || PathPrefix(`/favicon`) || PathPrefix(`/logo`) || Path(`/`))

# Backend  
traefik.http.routers.saltoestudia-backend.rule=Host(`saltoestudia.infra.com.uy`) && !PathPrefix(`/_next`) && !PathPrefix(`/favicon`) && !PathPrefix(`/logo`) && !Path(`/`)
```

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