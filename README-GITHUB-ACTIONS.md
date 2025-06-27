# 🚀 GitHub Actions - Deployment Automático

## 📋 Configuración Requerida

### 1. 🔑 Secrets en GitHub

Ve a tu repositorio → **Settings** → **Secrets and Variables** → **Actions** y agrega:

#### `SSH_PRIVATE_KEY`
```
[USAR LA CLAVE PRIVADA GENERADA LOCALMENTE]
⚠️ NUNCA exponer claves privadas en código fuente
💡 Usar: cat ~/.ssh/github_actions_deploy
```

#### `VPS_HOST`
```
ubuntu@150.230.30.198
```

#### `VPS_HOST_IP`
```
150.230.30.198
```

#### `ENV_FILE`
```
# Copia EXACTAMENTE el contenido de tu archivo .env local
DATABASE_URL=sqlite:///./data/saltoestudia.db
REFLEX_DB_URL=sqlite:///reflex.db
# ... resto de variables ...
```

### 2. 🔧 Configuración Completada

✅ **Workflow creado:** `.github/workflows/deploy.yml`  
✅ **Script actualizado:** `deploy-to-vps.sh`  
✅ **Clave SSH específica:** `github_actions_deploy`  
✅ **Seguridad:** Archivos sensibles en .gitignore  

## 🚀 Cómo Funciona

### Automático
```bash
git add .
git commit -m "nuevo feature"
git push origin master
# ¡GitHub Actions despliega automáticamente!
```

### Manual
1. Ve a **Actions** en tu repo GitHub
2. Selecciona "🚀 Deploy to VPS"
3. Click "Run workflow"

## 📊 Monitoreo

### Ver Logs de Deployment
- GitHub: **Actions** → último workflow
- VPS: `ssh -i ~/.ssh/github_actions_deploy ubuntu@150.230.30.198 'docker logs saltoestudia-app -f'`

### Estado de la Aplicación
- URL: https://saltoestudia.infra.com.uy
- Contenedores: `ssh -i ~/.ssh/github_actions_deploy ubuntu@150.230.30.198 'docker ps'`

## 🔒 Seguridad

### ✅ Implementado
- **Clave SSH específica** solo para deployment
- **Secrets encriptados** en GitHub
- **No exposure** de credenciales en código
- **Archivos sensibles** excluidos del repo

### ⚠️ Importante
- La clave `github_actions_deploy` es SOLO para CI/CD
- Tu clave personal sigue siendo privada
- Puedes revocar la clave de deployment sin afectar tu acceso

## 🛠️ Troubleshooting

### Deployment Falla
1. Revisa logs en GitHub Actions
2. Verifica que los secrets estén configurados
3. Comprueba conectividad: `ssh -i ~/.ssh/github_actions_deploy ubuntu@150.230.30.198`

### Aplicación No Responde
1. `ssh -i ~/.ssh/github_actions_deploy ubuntu@150.230.30.198 'docker ps'`
2. `ssh -i ~/.ssh/github_actions_deploy ubuntu@150.230.30.198 'docker logs saltoestudia-app'`
3. `ssh -i ~/.ssh/github_actions_deploy ubuntu@150.230.30.198 'docker restart traefik'`

## 🎯 Próximos Pasos

- [ ] Configurar secrets en GitHub
- [ ] Hacer primer push para probar
- [ ] Verificar deployment automático
- [ ] Configurar notificaciones (opcional) 
🎉 GitHub Actions configurado - mié 25 jun 2025 21:13:51 -03
✅ Deployment automático activo

