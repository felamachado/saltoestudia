# 🚀 DESPLIEGUE EN VPS ORACLE - SALTO ESTUDIA

Guía para desplegar Salto Estudia en VPS Oracle con Traefik + Docker.

## 📋 CONFIGURACIÓN ACTUAL DETECTADA

### ✅ VPS Oracle Cloud (150.230.30.198)
- **Traefik:** v2.11 con SSL automático (Let's Encrypt)
- **Ruta:** `/srv/docker/` 
- **Red:** `traefik-net` (externa)
- **Dominio base:** `*.infra.com.uy`

### ✅ Servicios existentes
- **Odoo:** `odoo.infra.com.uy`
- **Traefik Dashboard:** `traefik.infra.com.uy`
- **Portainer:** (gestión de contenedores)

---

## 🎯 CONFIGURACIÓN PARA SALTO ESTUDIA

### 🌐 URL Final
```
https://saltoestudia.infra.com.uy
```

### 📁 Estructura en VPS
```
/srv/docker/saltoestudia/
├── docker-compose.production.yml
├── dockerfile
├── .env (copiado de env.production.example)
├── data/
│   ├── saltoestudia.db (SQLite)
│   └── reflex.db
├── logs/
└── [código fuente]
```

---

## 🚀 DESPLIEGUE AUTOMÁTICO

### 1. Ejecutar script de despliegue
```bash
./deploy-to-vps.sh
```

### 2. El script automáticamente:
- ✅ Verifica conexión SSH
- ✅ Crea directorios en VPS
- ✅ Sincroniza código (rsync)
- ✅ Configura variables de entorno
- ✅ Construye imagen Docker
- ✅ Ejecuta contenedor con Traefik

---

## 🔧 COMANDOS MANUALES

### SSH al VPS
```bash
ssh ubuntu@150.230.30.198
```

### Gestión del servicio
```bash
cd /srv/docker/saltoestudia

# Ver logs
docker logs -f saltoestudia-app

# Reiniciar
docker-compose -f docker-compose.production.yml restart

# Reconstruir
docker-compose -f docker-compose.production.yml up -d --build

# Parar
docker-compose -f docker-compose.production.yml down
```

### Ver estado
```bash
docker ps | grep saltoestudia
curl -I https://saltoestudia.infra.com.uy
```

---

## ⚙️ CONFIGURACIÓN AVANZADA

### Variables de entorno importantes
```bash
DATABASE_URL=sqlite:///data/saltoestudia.db
REFLEX_ENV=production
```

### Labels de Traefik aplicados
```yaml
traefik.enable=true
traefik.http.routers.saltoestudia.rule=Host(`saltoestudia.infra.com.uy`)
traefik.http.routers.saltoestudia.entrypoints=websecure
traefik.http.routers.saltoestudia.tls.certresolver=letsencrypt
traefik.http.services.saltoestudia.loadbalancer.server.port=3000
```

---

## 🛠️ TROUBLESHOOTING

### Si no funciona el dominio:
1. Verificar que el contenedor esté corriendo: `docker ps`
2. Verificar logs: `docker logs saltoestudia-app`
3. Verificar Traefik: `curl -I https://traefik.infra.com.uy`

### Si hay problemas de permisos:
```bash
ssh ubuntu@150.230.30.198
sudo chown -R ubuntu:ubuntu /srv/docker/saltoestudia
```

### Ver logs de Traefik:
```bash
docker logs traefik
```

---

## 🔒 SEGURIDAD

### ✅ Configurado automáticamente:
- SSL/TLS con Let's Encrypt
- Redirección HTTP → HTTPS
- Headers de seguridad
- Firewall VPS (solo puertos 80, 443, 22)

### 🔐 Acceso administrativo:
- Panel: `https://saltoestudia.infra.com.uy`
- Usuarios: Ver `.env` para contraseñas 