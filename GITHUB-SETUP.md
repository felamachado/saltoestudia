# 🚀 Guía para Subir a GitHub - Salto Estudia

## ✅ Verificación de Seguridad Completada

### Archivos Protegidos:
- ✅ `.env` → Excluido de Git
- ✅ `data/*.db` → No se sube a GitHub
- ✅ Contraseñas → Solo en variables de entorno
- ✅ Credenciales → No hardcodeadas en código

---

## 📝 Pasos para Subir a GitHub

### 1. Preparar Commit:
```bash
git add .
git commit -m "feat: migrate to unified Docker setup + security improvements

- Replace docker-compose + start.sh with single dockerfile
- Add development (run-dev.sh) and production (run-prod.sh) scripts
- Improve security with proper .env exclusion
- Add comprehensive security documentation
- Maintain full backward compatibility"
```

### 2. Crear Repositorio en GitHub:
```bash
# Opción A: GitHub CLI
gh repo create saltoestudia --public --push

# Opción B: Manual
# 1. Ir a https://github.com/new
# 2. Crear repo "saltoestudia"
# 3. Ejecutar:
git remote add origin https://github.com/TU_USUARIO/saltoestudia.git
git branch -M main
git push -u origin main
```

### 3. Configurar Descripción del Repo:
```
🎓 Plataforma educativa para instituciones de Salto, Uruguay. 
Desarrollada con Reflex + SQLite, incluye gestión de cursos e instituciones.

🚀 Docker | 🔒 Seguro | 📱 Responsive
```

---

## 🔒 Checklist Final de Seguridad

Antes de hacer push, verificar:

- [ ] ✅ `.env` está en `.gitignore` 
- [ ] ✅ No hay contraseñas hardcodeadas
- [ ] ✅ `.env.example` disponible como template
- [ ] ✅ `SECURITY.md` incluido en el repo
- [ ] ✅ Base de datos no está en el repo
- [ ] ✅ Scripts Docker funcionando

---

## 📚 Documentación Incluida

El repo incluirá:
- `README.md` → Documentación principal
- `README-Docker.md` → Setup Docker
- `SECURITY.md` → Guía de seguridad
- `.env.example` → Template de configuración

---

## 🎯 Después de Subir

### Para colaboradores:
```bash
# 1. Clonar repo
git clone https://github.com/TU_USUARIO/saltoestudia.git
cd saltoestudia

# 2. Configurar entorno
cp .env.example .env
# Editar .env con contraseñas seguras

# 3. Ejecutar
./run-dev.sh
```

### Para producción:
- Configurar variables de entorno en el servidor
- Usar `./run-prod.sh` 
- Configurar HTTPS
- Monitorear logs

---

## 🚨 IMPORTANTE

**NUNCA subas**:
- Archivos `.env` 
- Bases de datos (*.db)
- Claves privadas (*.key, *.pem)
- Credenciales reales

**El proyecto está listo para GitHub con máxima seguridad!** 🛡️ 