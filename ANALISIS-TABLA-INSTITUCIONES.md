# 📊 Análisis de la Tabla de Instituciones - Salto Estudia

## 🏗️ Estructura de la Tabla `instituciones`

### 📋 Campos de la Tabla

| Campo | Tipo | Descripción | Restricciones |
|-------|------|-------------|---------------|
| `id` | INTEGER | Clave primaria autoincremental | PRIMARY KEY, NOT NULL |
| `nombre` | VARCHAR | Nombre oficial de la institución | NOT NULL |
| `logo` | VARCHAR | Ruta al archivo de logo | NULL permitido |

### 🔗 Relaciones con Otras Tablas

#### 1️⃣ Relación 1:N con `sedes`
- **Tabla**: `sedes`
- **Campo FK**: `institucion_id`
- **Restricción**: `NO ACTION` (no se puede eliminar una institución si tiene sedes)
- **Descripción**: Una institución puede tener múltiples sedes en diferentes ciudades

#### 2️⃣ Relación 1:N con `curso`
- **Tabla**: `curso`
- **Campo FK**: `institucion_id`
- **Restricción**: `NO ACTION` (no se puede eliminar una institución si tiene cursos)
- **Descripción**: Una institución puede ofrecer múltiples cursos

#### 3️⃣ Relación 1:N con `usuarios`
- **Tabla**: `usuarios`
- **Campo FK**: `institucion_id`
- **Restricción**: `NO ACTION` (no se puede eliminar una institución si tiene usuarios)
- **Descripción**: Una institución puede tener múltiples usuarios administradores

## 📊 Datos Actuales en la Base de Datos

### 🏢 Instituciones Registradas (6 total)

| ID | Nombre | Logo | Sedes | Cursos | Usuarios |
|----|--------|------|-------|--------|----------|
| 1 | UDELAR – CENUR LN | (vacío) | 10 | 10 | 10 |
| 2 | IAE Salto | `/logos/logoutu.png` | 6 | 6 | 6 |
| 3 | Esc. Catalina H. de Castaños | `/logos/logoutu.png` | 4 | 4 | 4 |
| 4 | Esc. De Administración | `/logos/logoutu.png` | 4 | 4 | 4 |
| 5 | Esc. Agraria | `/logos/logoutu.png` | 4 | 4 | 4 |
| 6 | Universidad de Montevideo | (vacío) | 4 | 0 | 4 |

### 📈 Estadísticas Generales
- **Total de instituciones**: 6
- **Total de sedes**: 18
- **Total de cursos**: 10
- **Total de usuarios**: 6

## 🎯 Características del Diseño

### ✅ Fortalezas del Modelo

#### 1. **Normalización Correcta**
- La tabla `instituciones` contiene solo datos específicos de la institución
- Los datos de contacto están separados en la tabla `sedes`
- Cada sede puede tener su propia información de contacto

#### 2. **Integridad Referencial**
- Claves foráneas con restricción `NO ACTION`
- Previene eliminación accidental de instituciones con datos relacionados
- Mantiene la consistencia de datos

#### 3. **Flexibilidad**
- Una institución puede tener múltiples sedes
- Cada sede puede estar en una ciudad diferente
- Permite gestión granular de información de contacto

### 🔍 Observaciones Importantes

#### 1. **Logos Inconsistentes**
- Algunas instituciones tienen logo vacío
- Otras usan el logo por defecto `/logos/logoutu.png`
- La primera institución (UDELAR) no tiene logo asignado

#### 2. **Distribución de Datos**
- La mayoría de instituciones tienen la misma cantidad de sedes, cursos y usuarios
- Solo "Universidad de Montevideo" no tiene cursos registrados
- "UDELAR – CENUR LN" es la institución con más datos (10 de cada)

#### 3. **Estructura de Relaciones**
- Relación 1:N bien implementada
- No hay relaciones many-to-many directas con instituciones
- Las relaciones many-to-many están en otras tablas (curso_ciudad)

## 💻 Uso en el Código

### 📁 Archivos que Utilizan la Tabla

#### 1. **`saltoestudia/models.py`**
```python
class Institucion(SQLModel, table=True):
    __tablename__ = "instituciones"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    logo: Optional[str] = None
    
    # Relaciones
    sedes: List["Sede"] = Relationship(back_populates="institucion")
    cursos: List["Curso"] = Relationship(back_populates="institucion")
    usuarios: List["Usuario"] = Relationship(back_populates="institucion")
```

#### 2. **`saltoestudia/database.py`**
- `obtener_instituciones()` - Lista todas las instituciones
- `obtener_instituciones_con_sedes_por_ciudad()` - Instituciones con sedes filtradas
- `obtener_institucion_por_id()` - Institución específica
- `modificar_institucion()` - Actualizar datos de institución

#### 3. **`saltoestudia/state.py`**
- Autenticación de usuarios por institución
- Filtrado de cursos por institución
- Gestión de sesión de administradores

### 🎨 Uso en la Interfaz

#### 1. **Página de Instituciones** (`pages/instituciones.py`)
- Muestra galería de instituciones
- Filtrado por ciudad
- Información de contacto por sede

#### 2. **Página de Cursos** (`pages/cursos.py`)
- Filtro por institución
- Búsqueda de cursos por institución

#### 3. **Panel de Administración** (`pages/admin.py`)
- CRUD de cursos por institución
- Gestión específica por usuario logueado

## 🔧 Operaciones Disponibles

### 📖 Operaciones de Lectura
- **Obtener todas las instituciones**
- **Obtener institución por ID**
- **Obtener instituciones con sedes**
- **Filtrar por ciudad**

### ✏️ Operaciones de Escritura
- **Modificar datos de institución** (nombre, logo)
- **No permite eliminación** (por restricciones de FK)

### 🔍 Operaciones de Consulta
- **Instituciones con cursos virtuales**
- **Instituciones con sedes físicas**
- **Conteo de relaciones**

## 🚀 Recomendaciones de Mejora

### 1. **Gestión de Logos**
- Implementar logo por defecto automático
- Validar rutas de archivos
- Considerar almacenamiento en base de datos

### 2. **Validaciones Adicionales**
- Validar formato de nombres
- Restricciones de longitud
- Validación de caracteres especiales

### 3. **Optimizaciones**
- Índices en campos de búsqueda
- Caché de consultas frecuentes
- Paginación para listas grandes

## 📝 Notas Técnicas

### Base de Datos
- **Tipo**: SQLite (desarrollo) / PostgreSQL (producción)
- **ORM**: SQLModel (combinación de SQLAlchemy + Pydantic)
- **Migraciones**: Alembic

### Seguridad
- **Integridad referencial**: Activada
- **Validaciones**: En capa de aplicación
- **Autenticación**: Por institución

### Rendimiento
- **Consultas optimizadas**: Sin eager loading innecesario
- **Relaciones lazy**: Carga bajo demanda
- **Índices**: En campos de búsqueda

---

**Fecha de análisis**: $(date)
**Base de datos**: `data/saltoestudia.db`
**Estado**: ✅ Funcionando correctamente 