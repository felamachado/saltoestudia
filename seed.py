# ================================================================================
# SCRIPT DE POBLADO INICIAL - SALTO ESTUDIA
# ================================================================================
#
# Este script inicializa la base de datos con datos fundamentales del sistema.
# Es crítico para el funcionamiento y debe ejecutarse después de las migraciones.
#
# PROPÓSITO:
# - Poblar instituciones educativas de Salto, Uruguay
# - Crear usuarios administradores con contraseñas individuales desde .env
# - Cargar cursos de ejemplo para cada institución
# - Verificar integridad de datos antes de proceder
#
# SISTEMA DE CONTRASEÑAS INDIVIDUALES:
# - Cada institución tiene su propia contraseña desde variables de entorno
# - Las contraseñas se hashean con bcrypt antes de almacenar
# - Sistema completamente seguro y escalable para producción
#
# EJECUCIÓN:
# - Desde Docker: docker compose exec app python seed.py
# - Desde local: python seed.py (requiere .env configurado)
# - Idempotente: puede ejecutarse múltiples veces sin duplicar datos
#
# ARCHIVOS RELACIONADOS:
# - .env: Contiene las contraseñas reales por institución
# - .env.example: Plantilla para el equipo de desarrollo
# - models.py: Define las estructuras de datos a poblar
# - constants.py: Valida los datos antes de insertar
# ================================================================================

import sqlite3
import bcrypt
import os

# ================================================================================
# FUNCIONES UTILITARIAS DE SEGURIDAD
# ================================================================================

def hash_password(password: str) -> str:
    """
    Hashea una contraseña usando bcrypt con salt automático.
    
    bcrypt es el estándar de la industria para hash de contraseñas porque:
    - Incluye salt automático (previene rainbow table attacks)
    - Es computacionalmente costoso (previene brute force)
    - El costo puede ajustarse con el tiempo según hardware disponible
    
    Args:
        password: Contraseña en texto plano
        
    Returns:
        str: Hash bcrypt seguro para almacenar en base de datos
        
    Utilizado en:
        - Creación inicial de usuarios administradores
        - Verificación posterior en state.py con bcrypt.checkpw()
    """
    hashed_bytes = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')

def get_password_for_user(env_var: str, default: str) -> str:
    """
    Obtiene contraseña desde variable de entorno o usa fallback por defecto.
    
    Este patrón permite:
    - Desarrollo local: usar contraseñas por defecto
    - Producción: usar contraseñas seguras desde .env
    - Flexibilidad: cada institución puede tener contraseña única
    
    Args:
        env_var: Nombre de la variable de entorno (ej: "CENUR_PASSWORD")
        default: Contraseña por defecto si no existe la variable
        
    Returns:
        str: Contraseña a usar para el usuario
        
    Patrón de uso:
        password = get_password_for_user("CENUR_PASSWORD", "default_pass")
    """
    return os.getenv(env_var, default)

# ================================================================================
# FUNCIÓN PRINCIPAL DE POBLADO
# ================================================================================

def seed_database():
    """
    Función principal que puebla la base de datos con datos iniciales.
    
    FLUJO DE EJECUCIÓN:
    1. Verificar si ya hay datos (idempotencia)
    2. Insertar instituciones educativas de Salto
    3. Crear usuarios administradores con contraseñas individuales
    4. Cargar cursos de ejemplo para cada institución
    5. Mostrar resumen de seguridad y recomendaciones
    
    DATOS CARGADOS:
    - 5 instituciones reales de Salto, Uruguay
    - 5 usuarios administradores (uno por institución)
    - 10 cursos de ejemplo distribuidos entre instituciones
    
    SEGURIDAD IMPLEMENTADA:
    - Contraseñas individuales por institución desde .env
    - Hash bcrypt para todas las contraseñas
    - Verificación de variables de entorno vs defaults
    - Logging detallado para auditoría
    
    IDEMPOTENCIA:
    - Verifica datos existentes antes de proceder
    - No duplica información si ya existe
    - Seguro ejecutar múltiples veces
    
    Returns:
        bool: True si exitoso, False si falló
    """
    db_path = "/app/data/saltoestudia.db"
    
    try:
        print("🔗 Conectando a la base de datos...")
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar si ya hay datos
        cursor.execute("SELECT COUNT(*) FROM instituciones")
        count_instituciones = cursor.fetchone()[0]
        
        if count_instituciones > 0:
            print(f"📊 La base de datos ya tiene datos ({count_instituciones} instituciones).")
            cursor.execute("SELECT COUNT(*) FROM usuarios")
            count_usuarios = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM cursos")
            count_cursos = cursor.fetchone()[0]
            print(f"   Usuarios: {count_usuarios}, Cursos: {count_cursos}")
            print("✅ Base de datos ya está poblada.")
            conn.close()
            return True
        
        print("🏢 Insertando instituciones...")
        
        instituciones = [
            ("UDELAR – CENUR LN", "Rivera 1350", "47334816", "comunicacion@unorte.edu.uy", "https://www.litoralnorte.udelar.edu.uy/", "/logos/logo-cenur.png"),
            ("IAE Salto", "Misiones 192", "47354602", "iaesalto@gmail.com", None, "/logos/logoutu.png"),
            ("Esc. Catalina H. de Castaños", "Varela 440", "47335987", "ttssalto@gmail.com", None, "/logos/logoutu.png"),
            ("Esc. De Administración", "Juan C. Gomez 351", "47323778", "etays.salto@gmail.com", None, "/logos/logoutu.png"),
            ("Esc. Agraria", "Ruta a Salto Grande S/N", "47322862", "esagrariasalto@gmail.com", None, "/logos/logoutu.png")
        ]
        
        for inst in instituciones:
            cursor.execute("""
                INSERT INTO instituciones (nombre, direccion, telefono, email, web, logo)
                VALUES (?, ?, ?, ?, ?, ?)
            """, inst)
            print(f"   ✅ {inst[0]}")
        
        print("👥 Insertando usuarios con contraseñas individuales...")
        
        # Obtener contraseña por defecto
        default_password = os.getenv("DEFAULT_SEED_PASSWORD", "CHANGE_THIS_PASSWORD_NOW")
        
        # Crear usuarios con contraseñas individuales desde .env
        usuarios_config = [
            {
                "email": "cenur@cenur.com",
                "env_var": "CENUR_PASSWORD",
                "institucion_id": 1,
                "institucion_nombre": "UDELAR – CENUR LN"
            },
            {
                "email": "iae@iae.com", 
                "env_var": "IAE_PASSWORD",
                "institucion_id": 2,
                "institucion_nombre": "IAE Salto"
            },
            {
                "email": "catalina@catalina.com",
                "env_var": "CATALINA_PASSWORD", 
                "institucion_id": 3,
                "institucion_nombre": "Esc. Catalina H. de Castaños"
            },
            {
                "email": "administracion@administracion.com",
                "env_var": "ADMINISTRACION_PASSWORD",
                "institucion_id": 4,
                "institucion_nombre": "Esc. De Administración"
            },
            {
                "email": "agraria@agraria.com",
                "env_var": "AGRARIA_PASSWORD",
                "institucion_id": 5,
                "institucion_nombre": "Esc. Agraria"
            }
        ]
        
        usuarios_insertados = []
        for config in usuarios_config:
            # Obtener contraseña individual o usar la por defecto
            password = get_password_for_user(config["env_var"], default_password)
            hashed_password = hash_password(password)
            
            usuario_data = (config["email"], hashed_password, config["institucion_id"])
            cursor.execute("""
                INSERT INTO usuarios (correo, password_hash, institucion_id)
                VALUES (?, ?, ?)
            """, usuario_data)
            
            usuarios_insertados.append({
                "email": config["email"],
                "institucion": config["institucion_nombre"],
                "env_var": config["env_var"],
                "has_custom_password": os.getenv(config["env_var"]) is not None
            })
            
            print(f"   ✅ {config['email']} - {config['institucion_nombre']}")
        
        print("📚 Insertando cursos...")
        
        cursos = [
            # UDELAR – CENUR LN (id=1)
            ("Licenciatura en Informática", "Universitario", "4", "años", "Bachillerato", "Programa con fuerte énfasis en desarrollo de software.", 1),
            ("Taller de Introducción a la Robótica", "Terciario", "6", "meses", "Ciclo básico", "Laboratorio con kits Arduino incluidos.", 1),
            
            # IAE Salto (id=2)
            ("Gestión de Emprendimientos", "Terciario", "5", "meses", "Bachillerato", "Plan de negocios y mentoría con incubadoras locales.", 2),
            ("Marketing Digital y E-Commerce", "Terciario", "4", "meses", "Ciclo básico", "Campañas reales en redes sociales.", 2),
            
            # Esc. Catalina H. de Castaños (id=3)
            ("Electricidad Domiciliaria", "Terciario", "4", "meses", "Ciclo básico", "Prácticas en instalaciones reales.", 3),
            ("Carpintería Básica", "Terciario", "6", "meses", "Ciclo básico", "Proyectos prácticos.", 3),
            
            # Esc. De Administración (id=4)
            ("Administración de Empresas", "Bachillerato", "3", "años", "Ciclo básico", "Formación integral en gestión empresarial.", 4),
            ("Contabilidad Básica", "Terciario", "6", "meses", "Ciclo básico", "Uso de software contable.", 4),
            
            # Esc. Agraria (id=5)
            ("Técnico Agropecuario", "Bachillerato", "3", "años", "Ciclo básico", "Prácticas en campo y laboratorio propio.", 5),
            ("Horticultura Orgánica", "Terciario", "8", "meses", "Ciclo básico", "Invernadero experimental.", 5)
        ]
        
        for curso in cursos:
            cursor.execute("""
                INSERT INTO cursos (nombre, nivel, duracion_numero, duracion_unidad, requisitos_ingreso, informacion, institucion_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, curso)
            print(f"   ✅ {curso[0]}")
        
        # Confirmar cambios
        conn.commit()
        
        print("\n🎉 ¡Base de datos poblada exitosamente!")
        print(f"📊 Se crearon {len(instituciones)} instituciones, {len(usuarios_insertados)} usuarios y {len(cursos)} cursos.")
        
        # Mostrar información de seguridad
        print("\n🔑 Usuarios creados con contraseñas individuales:")
        users_with_custom = 0
        for usuario in usuarios_insertados:
            status = "🔐 Personalizada" if usuario["has_custom_password"] else "⚠️ Por defecto"
            print(f"   📧 {usuario['email']}")
            print(f"      🏢 {usuario['institucion']}")
            print(f"      🔑 Variable: {usuario['env_var']} - {status}")
            if usuario["has_custom_password"]:
                users_with_custom += 1
        
        print(f"\n📊 Resumen de seguridad:")
        print(f"   ✅ Usuarios con contraseña personalizada: {users_with_custom}")
        print(f"   ⚠️ Usuarios con contraseña por defecto: {len(usuarios_insertados) - users_with_custom}")
        
        if users_with_custom < len(usuarios_insertados):
            print(f"\n⚠️  RECOMENDACIÓN DE SEGURIDAD:")
            print(f"   Algunos usuarios usan la contraseña por defecto.")
            print(f"   En producción, configura todas las variables en el .env")
        
        conn.close()
        return True
            
    except Exception as e:
        print(f"❌ Error durante el seed de la base de datos: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = seed_database()
    if success:
        print("\n✅ Seed completado exitosamente.")
    else:
        print("\n❌ Seed falló. Revisa los errores anteriores.")
        exit(1)