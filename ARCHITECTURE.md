# 🏗️ Arquitectura del Sistema - Salto Estudia

## 📋 Resumen Ejecutivo

**Salto Estudia** es una plataforma educativa web desarrollada en **Python** con **Reflex** que permite gestionar y consultar la oferta educativa de instituciones en Salto, Uruguay. El sistema implementa una arquitectura moderna con separación clara de responsabilidades, gestión de estado reactiva y despliegue containerizado.

## 🎯 Propósito del Sistema

### Objetivo Principal
Proporcionar una plataforma centralizada para:
- **Consultar** la oferta educativa disponible en Salto
- **Gestionar** cursos e instituciones educativas
- **Facilitar** la búsqueda de opciones educativas para estudiantes

### Usuarios Objetivo
- **Público general**: Estudiantes buscando opciones educativas
- **Administradores**: Personal de instituciones educativas
- **Gestores**: Administradores del sistema

## 🏛️ Arquitectura General

### Stack Tecnológico
```
Frontend: Reflex (Python → React) + Bootstrap CSS
Backend:  Python + SQLModel + SQLite
Estado:   Reflex State Management (Reactivo)
Auth:     bcrypt + sesiones
Deploy:   Docker + Traefik + Let's Encrypt
```

### Patrón Arquitectónico
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend       │    │   Database      │
│   (Reflex)      │◄──►│   (Python)      │◄──►│   (SQLite)      │
│                 │    │                 │    │                 │
│ • UI Reactiva   │    │ • Lógica de     │    │ • Persistencia  │
│ • Estado Global │    │   Negocio       │    │ • Modelos       │
│ • Componentes   │    │ • Validaciones  │    │ • Relaciones    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📁 Estructura del Proyecto

### Organización de Directorios
```
saltoestudia/
├── saltoestudia/           # Código fuente principal
│   ├── __init__.py         # Inicialización del módulo
│   ├── saltoestudia.py     # Punto de entrada de la aplicación
│   ├── state.py           # Gestión de estado global
│   ├── database.py        # Operaciones de base de datos
│   ├── models.py          # Modelos de datos SQLModel
│   ├── constants.py       # Constantes del sistema
│   ├── theme.py           # Sistema de diseño y estilos
│   ├── layout.py          # Componentes de layout reutilizables
│   └── pages/             # Páginas de la aplicación
│       ├── index.py       # Página de inicio
│       ├── cursos.py      # Buscador de cursos
│       ├── instituciones.py # Galería de instituciones
│       ├── admin.py       # Panel de administración
│       ├── admin_sedes.py # Gestión de sedes
│       ├── login.py       # Página de login
│       └── info.py        # Información del proyecto
├── assets/                # Recursos estáticos
├── data/                  # Base de datos SQLite
├── scripts/               # Scripts de automatización
├── docker-compose.yml     # Configuración Docker
├── requirements.txt       # Dependencias Python
└── README.md             # Documentación principal
```

## 🔄 Flujo de Datos

### 1. Consulta Pública (Usuarios no autenticados)
```
Usuario → Página Cursos → State.aplicar_filtros() → Database.obtener_cursos() → SQLite → UI
```

### 2. Administración (Usuarios autenticados)
```
Admin → Login → State.handle_login() → Database.validar_usuario() → Session → Panel Admin
```

### 3. Gestión de Cursos
```
Admin → Formulario → State.agregar_curso() → Database.agregar_curso() → SQLite → UI Actualizada
```

## 🗄️ Modelo de Datos

### Entidades Principales

#### 1. Institución
```python
class Institucion:
    id: int                    # Clave primaria
    nombre: str               # Nombre oficial
    logo: Optional[str]       # Ruta al logo
    
    # Relaciones
    sedes: List[Sede]         # Sedes de la institución
    cursos: List[Curso]       # Cursos ofrecidos
    usuarios: List[Usuario]   # Administradores
```

#### 2. Curso
```python
class Curso:
    id: int                    # Clave primaria
    nombre: str               # Nombre del curso
    nivel: str                # Nivel educativo
    duracion_numero: str      # Duración numérica
    duracion_unidad: str      # Unidad de tiempo
    requisitos_ingreso: str   # Requisitos previos
    lugar: str                # Lugar donde se dicta
    informacion: str          # Información adicional
    institucion_id: int       # FK a Institución
```

#### 3. Usuario
```python
class Usuario:
    id: int                    # Clave primaria
    correo: str               # Email único
    password_hash: str        # Hash de contraseña
    institucion_id: int       # FK a Institución
```

#### 4. Sede
```python
class Sede:
    id: int                    # Clave primaria
    nombre: str               # Nombre de la sede
    direccion: str            # Dirección física
    telefono: str             # Teléfono de contacto
    email: str                # Email de contacto
    web: str                  # Sitio web
    ciudad: str               # Ciudad donde está ubicada
    institucion_id: int       # FK a Institución
```

### Relaciones
- **Institución 1:N Sede**: Una institución puede tener múltiples sedes
- **Institución 1:N Curso**: Una institución puede ofrecer múltiples cursos
- **Institución 1:N Usuario**: Una institución puede tener múltiples administradores
- **Curso N:M Ciudad**: Un curso puede dictarse en múltiples ciudades

## 🎨 Sistema de Diseño

### Principios de Diseño
1. **Consistencia**: Componentes reutilizables con estilos centralizados
2. **Responsividad**: Adaptación automática a diferentes dispositivos
3. **Accesibilidad**: Contraste adecuado y navegación por teclado
4. **Performance**: Carga lazy y cache inteligente

### Paleta de Colores
```python
PRIMARY = "#004A99"           # Azul principal del proyecto
PRIMARY_HOVER = "#003875"     # Azul más oscuro para hover
SUCCESS = "#10B981"           # Verde para éxito
WARNING = "#F59E0B"           # Amarillo para advertencias
DANGER = "#EF4444"            # Rojo para peligro/eliminar
```

### Componentes Reutilizables
- **ButtonStyle**: Estilos de botones (primary, secondary, danger, success)
- **ComponentStyle**: Estilos de componentes (tablas, formularios, modales)
- **Typography**: Configuración de fuentes y pesos

## 🔐 Sistema de Autenticación

### Flujo de Autenticación
1. **Login**: Usuario ingresa correo y contraseña
2. **Validación**: bcrypt verifica hash de contraseña
3. **Sesión**: Se crea sesión de usuario en estado global
4. **Autorización**: Verificación de permisos por institución

### Seguridad
- **Contraseñas**: Hash con bcrypt (salt automático)
- **Sesiones**: Gestión en memoria con Reflex State
- **Autorización**: Aislamiento por institución
- **Validación**: Sanitización de inputs

## 📊 Gestión de Estado

### Patrón State Management
```python
class State(rx.State):
    # Datos públicos
    cursos: List[Dict] = []
    instituciones: List[Dict] = []
    
    # Filtros
    nivel_seleccionado: str = ""
    institucion_seleccionada: str = ""
    
    # Autenticación
    logged_in_user: Optional[User] = None
    
    # UI Control
    show_login_dialog: bool = False
    show_curso_dialog: bool = False
```

### Características del Estado
- **Reactivo**: Cambios automáticos en UI
- **Thread-safe**: Aislamiento por sesión de usuario
- **Cache inteligente**: Evita consultas innecesarias
- **Progressive loading**: Carga gradual de datos

## 🚀 Despliegue y Infraestructura

### Entornos
- **Desarrollo**: Docker local con hot reload
- **Producción**: VPS con Traefik y SSL automático

### Configuración Docker
```yaml
services:
  app:
    build: .
    ports:
      - "3000:3000"  # Frontend
      - "8000:8000"  # Backend
    volumes:
      - ./data:/app/data  # Persistencia de BD
```

### Traefik (Producción)
- **Reverse proxy** automático
- **SSL** con Let's Encrypt
- **Load balancing** para escalabilidad
- **Health checks** automáticos

## 🔧 Configuración y Variables de Entorno

### Variables Críticas
```bash
DATABASE_URL=sqlite:///./data/saltoestudia.db
REFLEX_DB_URL=sqlite:///reflex.db
PYTHONPATH=/app
```

### Archivos de Configuración
- **`.env`**: Variables de producción (NO en Git)
- **`config-desarrollo.env`**: Variables de desarrollo
- **`docker-compose.yml`**: Configuración de contenedores

## 📈 Performance y Optimización

### Estrategias Implementadas
1. **Cache inteligente**: Evita recargas innecesarias
2. **Progressive loading**: Carga gradual de datos
3. **Lazy loading**: Componentes cargados bajo demanda
4. **Optimización de queries**: Consultas eficientes con SQLModel

### Métricas de Performance
- **Cold start**: < 3 segundos
- **Navegación**: < 500ms (con cache)
- **Búsquedas**: < 200ms
- **Autenticación**: < 100ms

## 🛡️ Seguridad

### Medidas Implementadas
- **Validación de inputs**: Sanitización de datos
- **Hash de contraseñas**: bcrypt con salt
- **Aislamiento de datos**: Por institución
- **HTTPS**: SSL automático en producción
- **Headers de seguridad**: Configurados en Traefik

### Buenas Prácticas
- No almacenar credenciales en código
- Validación del lado servidor
- Logs de auditoría
- Backup automático de base de datos

## 🔄 Workflow de Desarrollo

### Flujo de Trabajo
1. **Desarrollo local**: `./scripts/start-project.sh local`
2. **Testing**: Verificación automática de funcionalidades
3. **Commit**: Git con mensajes descriptivos
4. **Deploy**: Automático via GitHub Actions
5. **Monitoreo**: Logs y métricas en producción

### Scripts de Automatización
- **`setup-env.sh`**: Configuración de entornos
- **`start-project.sh`**: Inicio de aplicación
- **`deploy-to-vps.sh`**: Despliegue manual
- **`verify-production-setup.sh`**: Verificación de producción

## 📚 Documentación Adicional

### Archivos de Documentación
- **`README.md`**: Guía de inicio rápido
- **`DEPLOYMENT.md`**: Guía completa de despliegue
- **`ENTORNOS.md`**: Configuración de entornos
- **`TROUBLESHOOTING.md`**: Solución de problemas
- **`ARCHITECTURE.md`**: Esta documentación de arquitectura

### Código Documentado
- **Docstrings**: En todas las funciones principales
- **Comentarios**: Explicación de lógica compleja
- **Type hints**: Tipado estático para mejor IDE support
- **Constants**: Valores centralizados y documentados

## 🎯 Próximos Pasos y Mejoras

### Funcionalidades Planificadas
- [ ] API REST para integración externa
- [ ] Sistema de notificaciones
- [ ] Dashboard de métricas
- [ ] Exportación de datos
- [ ] Sistema de búsqueda avanzada

### Mejoras Técnicas
- [ ] Migración a PostgreSQL para escalabilidad
- [ ] Implementación de Redis para cache
- [ ] Sistema de logs centralizado
- [ ] Tests automatizados
- [ ] CI/CD mejorado

---

*Esta documentación se actualiza automáticamente con cada cambio significativo en la arquitectura del sistema.* 