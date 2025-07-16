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

import bcrypt
import os
from sqlmodel import create_engine, Session, select
from saltoestudia.models import Institucion, Usuario, Curso, Ciudad, CursoCiudadLink, Sede
from saltoestudia.database import engine

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
    
    try:
        print("🔗 Conectando a la base de datos...")
        
        with Session(engine) as session:
            # Verificar si ya hay datos
            instituciones_count = session.exec(select(Institucion)).all()
            
            if len(instituciones_count) > 0:
                print(f"📊 La base de datos ya tiene datos ({len(instituciones_count)} instituciones).")
                usuarios_count = session.exec(select(Usuario)).all()
                cursos_count = session.exec(select(Curso)).all()
                print(f"   Usuarios: {len(usuarios_count)}, Cursos: {len(cursos_count)}")
                print("✅ Base de datos ya está poblada.")
                return True
            
            print("🏢 Insertando instituciones...")
            
            # Verificar o crear la ciudad 'Salto'
            ciudad_salto = session.exec(select(Ciudad).where(Ciudad.nombre == "Salto")).first()
            if not ciudad_salto:
                ciudad_salto = Ciudad(nombre="Salto")
                session.add(ciudad_salto)
                session.commit()
                session.refresh(ciudad_salto)

            # Datos de las instituciones con sus sedes
            instituciones_data = [
                {
                    "nombre": "UDELAR – CENUR LN",
                    "logo": "/logos/logo-cenur.png",
                    "sede": {
                        "direccion": "Rivera 1350",
                        "telefono": "47334816",
                        "email": "comunicacion@unorte.edu.uy",
                        "web": "https://www.litoralnorte.udelar.edu.uy/"
                    }
                },
                {
                    "nombre": "IAE Salto",
                    "logo": "/logos/logoutu.png",
                    "sede": {
                        "direccion": "Misiones 192",
                        "telefono": "47354602",
                        "email": "iaesalto@gmail.com",
                        "web": None
                    }
                },
                {
                    "nombre": "Esc. Catalina H. de Castaños",
                    "logo": "/logos/logoutu.png",
                    "sede": {
                        "direccion": "Varela 440",
                        "telefono": "47335987",
                        "email": "ttssalto@gmail.com",
                        "web": None
                    }
                },
                {
                    "nombre": "Esc. De Administración",
                    "logo": "/logos/logoutu.png",
                    "sede": {
                        "direccion": "Juan C. Gomez 351",
                        "telefono": "47323778",
                        "email": "etays.salto@gmail.com",
                        "web": None
                    }
                },
                {
                    "nombre": "Esc. Agraria",
                    "logo": "/logos/logoutu.png",
                    "sede": {
                        "direccion": "Ruta a Salto Grande S/N",
                        "telefono": "47322862",
                        "email": "esagrariasalto@gmail.com",
                        "web": None
                    }
                },
                {
                    "nombre": "Universidad de Montevideo",
                    "logo": "/logos/logoutu.png",
                    "sede": {
                        "direccion": "Av. 18 de Julio 1968",
                        "telefono": "27074444",
                        "email": "info@um.edu.uy",
                        "web": "https://www.um.edu.uy/"
                    }
                }
            ]
            
            for i, inst_data in enumerate(instituciones_data):
                # Crear institución
                institucion = Institucion(
                    nombre=inst_data["nombre"],
                    logo=inst_data["logo"]
                )
                session.add(institucion)
                session.commit()  # Para obtener el id de la institución
                session.refresh(institucion)
                print(f"   ✅ {institucion.nombre}")
                
                # Determinar ciudad según la institución
                if inst_data["nombre"] == "Universidad de Montevideo":
                    ciudad_montevideo = session.exec(select(Ciudad).where(Ciudad.nombre == "Montevideo")).first()
                    if not ciudad_montevideo:
                        ciudad_montevideo = Ciudad(nombre="Montevideo")
                        session.add(ciudad_montevideo)
                        session.commit()
                        session.refresh(ciudad_montevideo)
                    ciudad_id = ciudad_montevideo.id
                    ciudad_nombre = "Montevideo"
                else:
                    ciudad_id = ciudad_salto.id
                    ciudad_nombre = "Salto"
                # Crear sede física principal
                sede = Sede(
                    institucion_id=institucion.id,
                    ciudad_id=ciudad_id,
                    direccion=inst_data["sede"]["direccion"],
                    telefono=inst_data["sede"]["telefono"],
                    email=inst_data["sede"]["email"],
                    web=inst_data["sede"]["web"]
                )
                session.add(sede)
                print(f"      🏢 Sede creada para {institucion.nombre} en {ciudad_nombre}")
                
                # Agregar sedes adicionales para algunas instituciones
                if inst_data["nombre"] == "UDELAR – CENUR LN":
                    # Crear ciudades para UDELAR CENUR LN
                    ciudades_udelar = ["Artigas", "Paysandú", "Río Negro"]
                    for ciudad_nombre in ciudades_udelar:
                        ciudad = session.exec(select(Ciudad).where(Ciudad.nombre == ciudad_nombre)).first()
                        if not ciudad:
                            ciudad = Ciudad(nombre=ciudad_nombre)
                            session.add(ciudad)
                            session.commit()
                            session.refresh(ciudad)
                        
                        # Datos específicos para cada sede
                        sedes_udelar = {
                            "Artigas": {
                                "direccion": "Av. Artigas 1234",
                                "telefono": "47721234",
                                "email": "artigas@unorte.edu.uy",
                                "web": "https://www.litoralnorte.udelar.edu.uy/artigas"
                            },
                            "Paysandú": {
                                "direccion": "Av. Artigas 567",
                                "telefono": "47221234",
                                "email": "paysandu@unorte.edu.uy",
                                "web": "https://www.litoralnorte.udelar.edu.uy/paysandu"
                            },
                            "Río Negro": {
                                "direccion": "Av. Artigas 890",
                                "telefono": "45621234",
                                "email": "rionegro@unorte.edu.uy",
                                "web": "https://www.litoralnorte.udelar.edu.uy/rionegro"
                            }
                        }
                        
                        sede_data = sedes_udelar[ciudad_nombre]
                        sede = Sede(
                            institucion_id=institucion.id,
                            ciudad_id=ciudad.id,
                            direccion=sede_data["direccion"],
                            telefono=sede_data["telefono"],
                            email=sede_data["email"],
                            web=sede_data["web"]
                        )
                        session.add(sede)
                        print(f"      🏢 Sede adicional creada para {institucion.nombre} en {ciudad_nombre}")
                
                elif inst_data["nombre"] == "Universidad de Montevideo":
                    # Crear ciudades para Universidad de Montevideo
                    ciudades_um = ["Punta del Este", "Colonia"]
                    for ciudad_nombre in ciudades_um:
                        ciudad = session.exec(select(Ciudad).where(Ciudad.nombre == ciudad_nombre)).first()
                        if not ciudad:
                            ciudad = Ciudad(nombre=ciudad_nombre)
                            session.add(ciudad)
                            session.commit()
                            session.refresh(ciudad)
                        
                        # Datos específicos para cada sede
                        sedes_um = {
                            "Punta del Este": {
                                "direccion": "Av. Roosevelt 1234",
                                "telefono": "42481234",
                                "email": "puntadeleste@um.edu.uy",
                                "web": "https://www.um.edu.uy/punta-del-este"
                            },
                            "Colonia": {
                                "direccion": "Av. General Flores 567",
                                "telefono": "45221234",
                                "email": "colonia@um.edu.uy",
                                "web": "https://www.um.edu.uy/colonia"
                            }
                        }
                        
                        sede_data = sedes_um[ciudad_nombre]
                        sede = Sede(
                            institucion_id=institucion.id,
                            ciudad_id=ciudad.id,
                            direccion=sede_data["direccion"],
                            telefono=sede_data["telefono"],
                            email=sede_data["email"],
                            web=sede_data["web"]
                        )
                        session.add(sede)
                        print(f"      🏢 Sede adicional creada para {institucion.nombre} en {ciudad_nombre}")
                
                elif inst_data["nombre"] == "IAE Salto":
                    # Agregar sede en Rivera
                    ciudad_rivera = session.exec(select(Ciudad).where(Ciudad.nombre == "Rivera")).first()
                    if not ciudad_rivera:
                        ciudad_rivera = Ciudad(nombre="Rivera")
                        session.add(ciudad_rivera)
                        session.commit()
                        session.refresh(ciudad_rivera)
                    
                    sede_rivera = Sede(
                        institucion_id=institucion.id,
                        ciudad_id=ciudad_rivera.id,
                        direccion="Sarandí 567",
                        telefono="46212345",
                        email="rivera@iae.edu.uy",
                        web=None
                    )
                    session.add(sede_rivera)
                    print(f"      🏢 Sede adicional creada para {institucion.nombre} en Rivera")
                # Crear sede virtual para todas las instituciones
                ciudad_virtual = session.exec(select(Ciudad).where(Ciudad.nombre == "Virtual")).first()
                if not ciudad_virtual:
                    ciudad_virtual = Ciudad(nombre="Virtual")
                    session.add(ciudad_virtual)
                    session.commit()
                    session.refresh(ciudad_virtual)
                sede_virtual = Sede(
                    institucion_id=institucion.id,
                    ciudad_id=ciudad_virtual.id,
                    direccion="Modalidad online/remota",
                    telefono="",
                    email=inst_data["sede"]["email"],
                    web=inst_data["sede"]["web"]
                )
                session.add(sede_virtual)
                print(f"      🏢 Sede virtual creada para {institucion.nombre}")
            session.commit()
            
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
                },
                {
                    "email": "um@um.edu.uy",
                    "env_var": "UM_PASSWORD",
                    "institucion_id": 6,
                    "institucion_nombre": "Universidad de Montevideo"
                }
            ]
            
            usuarios_insertados = []
            for config in usuarios_config:
                # Obtener contraseña individual o usar la por defecto
                password = get_password_for_user(config["env_var"], default_password)
                hashed_password = hash_password(password)
                
                usuario = Usuario(
                    correo=config["email"],
                    password_hash=hashed_password,
                    institucion_id=config["institucion_id"]
                )
                session.add(usuario)
                
                usuarios_insertados.append({
                    "email": config["email"],
                    "institucion": config["institucion_nombre"],
                    "env_var": config["env_var"],
                    "has_custom_password": os.getenv(config["env_var"]) is not None
                })
                
                print(f"   ✅ {config['email']} - {config['institucion_nombre']}")
            
            session.commit()
            
            print("🏙️ Insertando ciudades...")
            # Crear ciudades (capitales departamentales + Virtual)
            ciudades = [
                "Virtual", "Artigas", "Canelones", "Melo", "Colonia del Sacramento", "Durazno", "Trinidad", "Florida", "Minas", "Maldonado", "Paysandú", "Fray Bentos", "Rivera", "Rocha", "San José de Mayo", "Mercedes", "Tacuarembó", "Treinta y Tres"
            ]
            ciudad_objs = []
            for nombre in ciudades:
                ciudad_existente = session.exec(select(Ciudad).where(Ciudad.nombre == nombre)).first()
                if ciudad_existente:
                    ciudad_objs.append(ciudad_existente)
                    print(f"   ⚠️  {nombre} ya existe, no se crea de nuevo.")
                else:
                    ciudad = Ciudad(nombre=nombre)
                    session.add(ciudad)
                    ciudad_objs.append(ciudad)
                    print(f"   ✅ {nombre}")
            
            session.commit()
            
            # Agregar la ciudad Salto (que ya existe) al inicio de la lista
            ciudad_objs.insert(0, ciudad_salto)
            
            print("📚 Insertando cursos...")
            
            # === NUEVO: Mapear ciudades válidas por institución ===
            instituciones_sedes = {}
            for inst in session.exec(select(Institucion)).all():
                sedes = session.exec(select(Sede).where(Sede.institucion_id == inst.id)).all()
                ciudades_validas = [session.exec(select(Ciudad).where(Ciudad.id == sede.ciudad_id)).first().nombre for sede in sedes]
                instituciones_sedes[inst.id] = set(ciudades_validas)
            
            # Definir cursos con sus ciudades (usando nombres, no índices)
            cursos_data = [
                # UDELAR – CENUR LN (id=1)
                {
                    "nombre": "Licenciatura en Informática",
                    "nivel": "Universitario",
                    "duracion_numero": "4",
                    "duracion_unidad": "años",
                    "requisitos_ingreso": "Bachillerato",
                    "informacion": "Programa con fuerte énfasis en desarrollo de software.",
                    "institucion_id": 1,
                    "ciudades": ["Salto", "Virtual"]
                },
                {
                    "nombre": "Taller de Introducción a la Robótica",
                    "nivel": "Terciario",
                    "duracion_numero": "6",
                    "duracion_unidad": "meses",
                    "requisitos_ingreso": "Ciclo básico",
                    "informacion": "Laboratorio con kits Arduino incluidos.",
                    "institucion_id": 1,
                    "ciudades": ["Salto", "Virtual"]
                },
                
                # IAE Salto (id=2)
                {
                    "nombre": "Gestión de Emprendimientos",
                    "nivel": "Terciario",
                    "duracion_numero": "5",
                    "duracion_unidad": "meses",
                    "requisitos_ingreso": "Bachillerato",
                    "informacion": "Plan de negocios y mentoría con incubadoras locales.",
                    "institucion_id": 2,
                    "ciudades": ["Salto", "Virtual"]
                },
                {
                    "nombre": "Marketing Digital y E-Commerce",
                    "nivel": "Terciario",
                    "duracion_numero": "4",
                    "duracion_unidad": "meses",
                    "requisitos_ingreso": "Ciclo básico",
                    "informacion": "Campañas reales en redes sociales.",
                    "institucion_id": 2,
                    "ciudades": ["Salto", "Virtual"]
                },
                
                # Esc. Catalina H. de Castaños (id=3)
                {
                    "nombre": "Electricidad Domiciliaria",
                    "nivel": "Terciario",
                    "duracion_numero": "4",
                    "duracion_unidad": "meses",
                    "requisitos_ingreso": "Ciclo básico",
                    "informacion": "Prácticas en instalaciones reales.",
                    "institucion_id": 3,
                    "ciudades": ["Salto", "Virtual"]
                },
                {
                    "nombre": "Carpintería Básica",
                    "nivel": "Terciario",
                    "duracion_numero": "6",
                    "duracion_unidad": "meses",
                    "requisitos_ingreso": "Ciclo básico",
                    "informacion": "Proyectos prácticos.",
                    "institucion_id": 3,
                    "ciudades": ["Salto", "Virtual"]
                },
                
                # Esc. De Administración (id=4)
                {
                    "nombre": "Administración de Empresas",
                    "nivel": "Bachillerato",
                    "duracion_numero": "3",
                    "duracion_unidad": "años",
                    "requisitos_ingreso": "Ciclo básico",
                    "informacion": "Formación integral en gestión empresarial.",
                    "institucion_id": 4,
                    "ciudades": ["Salto", "Virtual"]
                },
                {
                    "nombre": "Contabilidad Básica",
                    "nivel": "Terciario",
                    "duracion_numero": "6",
                    "duracion_unidad": "meses",
                    "requisitos_ingreso": "Ciclo básico",
                    "informacion": "Uso de software contable.",
                    "institucion_id": 4,
                    "ciudades": ["Salto", "Virtual"]
                },
                
                # Esc. Agraria (id=5)
                {
                    "nombre": "Técnico Agropecuario",
                    "nivel": "Bachillerato",
                    "duracion_numero": "3",
                    "duracion_unidad": "años",
                    "requisitos_ingreso": "Ciclo básico",
                    "informacion": "Prácticas en campo y laboratorio propio.",
                    "institucion_id": 5,
                    "ciudades": ["Salto", "Virtual"]
                },
                {
                    "nombre": "Horticultura Orgánica",
                    "nivel": "Terciario",
                    "duracion_numero": "8",
                    "duracion_unidad": "meses",
                    "requisitos_ingreso": "Ciclo básico",
                    "informacion": "Invernadero experimental.",
                    "institucion_id": 5,
                    "ciudades": ["Salto", "Virtual"]
                }
            ]
            # Validar y poblar cursos solo con ciudades válidas
            for curso_data in cursos_data:
                ciudades_validas = instituciones_sedes[curso_data["institucion_id"]]
                ciudades_final = [c for c in curso_data["ciudades"] if c in ciudades_validas]
                if not ciudades_final:
                    print(f"⚠️  Curso '{curso_data['nombre']}' no tiene ciudades válidas para la institución. No se insertará.")
                    continue
                ciudad_objs_final = [session.exec(select(Ciudad).where(Ciudad.nombre == c)).first() for c in ciudades_final]
                curso = Curso(
                    nombre=curso_data["nombre"],
                    nivel=curso_data["nivel"],
                    duracion_numero=curso_data["duracion_numero"],
                    duracion_unidad=curso_data["duracion_unidad"],
                    requisitos_ingreso=curso_data["requisitos_ingreso"],
                    informacion=curso_data["informacion"],
                    institucion_id=curso_data["institucion_id"]
                )
                curso.ciudades = ciudad_objs_final
                session.add(curso)
                print(f"   ✅ {curso.nombre} ({', '.join(ciudades_final)})")
            session.commit()
            
            print("\n🎉 ¡Base de datos poblada exitosamente!")
            print(f"📊 Se crearon {len(instituciones_data)} instituciones, {len(usuarios_insertados)} usuarios y {len(cursos_data)} cursos.")
            
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