# 🐳 Flujo de Desarrollo con Docker

## ⚠️ IMPORTANTE: NO EJECUTES REFLEX LOCALMENTE

Este proyecto está **diseñado exclusivamente para Docker**. Ejecutar Reflex localmente causa conflictos de entornos, permisos y configuración.

## ✅ Flujo Correcto de Desarrollo

### 1. Después de hacer cambios en el código

```bash
# Bajar contenedores
docker compose down

# Reconstruir con los cambios
docker compose up --build -d

# Verificar que funciona
curl http://localhost:3000/instituciones
```

### 2. Verificar logs si hay problemas

```bash
# Ver logs en tiempo real
docker compose logs -f

# Ver logs solo de la aplicación
docker compose logs app
```

### 3. Debugging dentro del contenedor

```bash
# Entrar al contenedor
docker compose exec app bash

# Verificar base de datos
python3 -c "from saltoestudia.database import obtener_sedes_como_tarjetas; print(len(obtener_sedes_como_tarjetas()))"

# Verificar archivos
ls -la
```

## ❌ NO HACER (Causa Confusión)

### Comandos que NO debes ejecutar:

```bash
# ❌ NO ejecutar Reflex localmente
# python3 -m reflex run
# python3 -m reflex run --loglevel debug

# ❌ NO usar scripts que mezclen entornos
bash scripts/arrancar_dev.sh
bash scripts/arrancar_app.sh

# ❌ NO modificar la base de datos directamente
rm reflex.db
python3 init_db.py
python3 seed.py
```

### ¿Por qué NO funcionan estos comandos?

1. **Conflicto de entornos**: Docker tiene su propia configuración de base de datos, puertos y dependencias
2. **Permisos**: Los archivos pueden tener permisos diferentes entre Docker y local
3. **Configuración**: Docker usa variables de entorno específicas
4. **Puertos**: Pueden estar ocupados por el contenedor Docker

## 🔧 Comandos Útiles de Docker

### Gestión de Contenedores

```bash
# Ver estado de contenedores
docker compose ps

# Ver logs
docker compose logs -f

# Reiniciar solo la aplicación
docker compose restart app

# Parar completamente
docker compose down

# Parar y eliminar volúmenes (cuidado: borra datos)
docker compose down -v
```

### Debugging

```bash
# Entrar al contenedor
docker compose exec app bash

# Ver variables de entorno
docker compose exec app env

# Verificar base de datos
docker compose exec app ls -la /app/data/

# Ejecutar comandos Python
docker compose exec app python3 -c "import saltoestudia.database; print('OK')"
```

### Reconstrucción

```bash
# Reconstruir sin cache (si hay cambios en requirements.txt)
docker compose build --no-cache

# Reconstruir y levantar
docker compose up --build -d

# Forzar recreación de contenedores
docker compose up --build --force-recreate -d
```

## 🗄️ Base de Datos en Docker

### Ubicación
- **Dentro del contenedor**: `/app/data/saltoestudia.db`
- **En tu máquina**: `./data/saltoestudia.db` (volumen montado)

### Operaciones de Base de Datos

```bash
# Verificar que la base existe
docker compose exec app ls -la /app/data/

# Verificar contenido de la base
docker compose exec app python3 -c "from saltoestudia.database import obtener_sedes_como_tarjetas; print(f'Sedes: {len(obtener_sedes_como_tarjetas())}')"

# Aplicar migraciones (si es necesario)
docker compose exec app alembic upgrade head

# Ejecutar seed (si es necesario)
docker compose exec app python3 seed.py
```

## 🚨 Solución de Problemas

### Problema: "Connection Error" en la página web

```bash
# 1. Verificar que el contenedor esté corriendo
docker compose ps

# 2. Ver logs para errores
docker compose logs app

# 3. Reconstruir si es necesario
docker compose up --build -d
```

### Problema: Base de datos no se carga

```bash
# 1. Verificar volumen
docker compose exec app ls -la /app/data/

# 2. Verificar permisos
docker compose exec app ls -la /app/

# 3. Recrear base de datos si es necesario
docker compose down -v
docker compose up --build -d
```

### Problema: Cambios no se reflejan

```bash
# 1. Verificar que el código esté montado
docker compose exec app ls -la /app/saltoestudia/

# 2. Reconstruir contenedor
docker compose up --build -d

# 3. Verificar hot reload
docker compose logs -f
```

## 📋 Checklist de Desarrollo

Antes de empezar a trabajar:

- [ ] ✅ Contenedor Docker está corriendo
- [ ] ✅ Página web responde en http://localhost:3000
- [ ] ✅ Base de datos está montada correctamente
- [ ] ✅ Logs no muestran errores críticos

Después de hacer cambios:

- [ ] ✅ Ejecutar `docker compose down`
- [ ] ✅ Ejecutar `docker compose up --build -d`
- [ ] ✅ Verificar que la página funciona
- [ ] ✅ Verificar que los cambios se aplicaron

## 🔄 Flujo Completo de Desarrollo

### 1. Inicio de sesión de desarrollo

```bash
# Navegar al proyecto
cd /home/felipe/Escritorio/Proyectos/saltoestudia

# Verificar estado
docker compose ps

# Si no está corriendo, levantar
docker compose up -d
```

### 2. Durante el desarrollo

```bash
# Hacer cambios en el código
# ... editar archivos ...

# Reconstruir con cambios
docker compose down
docker compose up --build -d

# Verificar cambios
curl http://localhost:3000/instituciones
```

### 3. Debugging

```bash
# Ver logs en tiempo real
docker compose logs -f

# Entrar al contenedor si es necesario
docker compose exec app bash
```

### 4. Fin de sesión

```bash
# Opcional: parar contenedores
docker compose down

# O dejar corriendo para próxima sesión
# (los contenedores persisten)
```

## 📝 Notas Importantes

1. **Docker es el entorno oficial**: No hay soporte para desarrollo local directo
2. **Hot reload funciona**: Los cambios en el código se reflejan automáticamente
3. **Base de datos persiste**: Los datos se mantienen entre reinicios
4. **Puertos 3000 y 8000**: Reservados para Docker, no usar localmente
5. **Volúmenes**: El código y datos están montados desde tu máquina

## 🆘 Si Algo No Funciona

1. **Revisar logs**: `docker compose logs app`
2. **Reconstruir**: `docker compose up --build -d`
3. **Limpiar todo**: `docker compose down -v && docker compose up --build -d`
4. **Verificar Docker**: `docker --version && docker compose version`

---

**Recuerda**: Siempre usa Docker. Es más fácil, más confiable y evita problemas de configuración. 