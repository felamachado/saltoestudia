# Guía de Seguridad - Salto Estudia

## 🔒 Configuración Segura

### 1. Variables de Entorno
```bash
# Copia el template
cp .env.example .env

# Edita .env con contraseñas seguras
nano .env
```

### 2. Contraseñas Recomendadas
- **Mínimo**: 12 caracteres
- **Incluir**: Mayúsculas, minúsculas, números, símbolos
- **Evitar**: Información personal, palabras del diccionario
- **Ejemplo**: `K8#mN9$pL2@qX5!`

### 3. Archivos Protegidos
```
.env                    # ← NUNCA subir a GitHub
.env.*                  # ← Variables de entorno
data/*.db              # ← Bases de datos
*.key, *.pem           # ← Claves privadas
```

## 🚀 Deployment Seguro

### Desarrollo Local:
```bash
# 1. Configurar entorno
cp .env.example .env
# Editar .env con contraseñas seguras

# 2. Ejecutar
./run-dev.sh
```

### Producción:
```bash
# 1. Variables de entorno del servidor
export DATABASE_URL="postgresql://..."
export CENUR_PASSWORD="contraseña_super_segura"
# ... otras variables

# 2. Ejecutar
./run-prod.sh
```

## ⚠️ Checklist de Seguridad

### Antes de subir a GitHub:
- [ ] `.env` está en `.gitignore`
- [ ] No hay contraseñas en el código
- [ ] `.env.example` no tiene credenciales reales
- [ ] Database no está en el repo

### En producción:
- [ ] Variables de entorno configuradas
- [ ] HTTPS habilitado
- [ ] Contraseñas cambiadas regularmente
- [ ] Logs de acceso monitoreados

## 🛡️ Buenas Prácticas

### Contraseñas:
```bash
# Generar contraseña segura
openssl rand -base64 32
```

### Base de Datos:
```bash
# Backup seguro
sqlite3 data/saltoestudia.db ".backup backup_$(date +%Y%m%d).db"
```

### Monitoreo:
```bash
# Ver logs de acceso
docker logs saltoestudia-app | grep "POST\|login"
```

## 📞 Reporte de Vulnerabilidades

Si encuentras un problema de seguridad:
1. **NO** abras un issue público
2. Contacta directamente al desarrollador
3. Incluye detalles del problema
4. Espera respuesta antes de divulgar

---

**🔐 Nota**: Este proyecto usa bcrypt para hash de contraseñas y variables de entorno para credenciales. Mantén tu `.env` seguro y nunca lo subas a control de versiones. 