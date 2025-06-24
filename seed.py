from sqlmodel import Session, select
import reflex as rx
import bcrypt
import os
from sqlmodel import select, delete
# Importamos ambos modelos, Institucion y Usuario
from saltoestudia.models import Institucion, Usuario, Curso
from saltoestudia.constants import CursosConstants
from saltoestudia.database import agregar_curso, engine  # Ahora sí se puede importar

def hash_password(password: str) -> str:
    """Hashea una contraseña usando bcrypt."""
    # El salt se genera y se incluye en el hash final
    hashed_bytes = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')

def get_default_seed_password():
    """
    Obtiene la contraseña por defecto para los usuarios de seed desde variables de entorno.
    Si no está definida, usa una contraseña temporal que debe cambiarse.
    """
    return os.getenv("DEFAULT_SEED_PASSWORD", "temporal_cambiar_2024!")

def create_tables_if_not_exist():
    """Crea las tablas si no existen usando Reflex."""
    try:
        print("🔧 Verificando y creando tablas si es necesario...")
        # En Reflex 0.7.14, usar get_db_engine() en lugar de rx.engine
        engine = rx.Model.get_db_engine()
        rx.Model.metadata.create_all(bind=engine)
        print("✅ Tablas verificadas/creadas correctamente.")
        return True
    except Exception as e:
        print(f"❌ Error al crear tablas: {e}")
        return False

def seed_database():
    """
    Script idempotente para limpiar y poblar las tablas de instituciones y usuarios.
    
    IMPORTANTE: Este script crea usuarios con contraseñas por defecto.
    En producción, cambiar todas las contraseñas inmediatamente.
    """
    # Primero asegurar que las tablas existen
    if not create_tables_if_not_exist():
        print("❌ No se pudieron crear las tablas. Abortando seed.")
        return False

    try:
        with Session(engine) as session:
            # 1. Limpiar las tablas en el orden correcto (hijos antes que padres)
            print("🧹 Limpiando la tabla 'usuarios'...")
            try:
                session.exec(delete(Usuario))
                print("✅ Tabla 'usuarios' limpiada.")
            except Exception as e:
                print(f"⚠️ Error al limpiar usuarios (tabla puede no existir): {e}")
            
            print("🧹 Limpiando la tabla 'instituciones'...")
            try:
                session.exec(delete(Institucion))
                print("✅ Tabla 'instituciones' limpiada.")
            except Exception as e:
                print(f"⚠️ Error al limpiar instituciones (tabla puede no existir): {e}")
            
            # 2. Crear las 5 Instituciones
            print("🏢 Creando las 5 instituciones iniciales...")
            
            institucion1 = Institucion(
                nombre="UDELAR – CENUR LN",
                direccion="Rivera 1350",
                telefono="47334816",
                email="comunicacion@unorte.edu.uy",
                web="https://www.litoralnorte.udelar.edu.uy/",
                logo="/logos/logo-cenur.png"
            )
            
            institucion2 = Institucion(
                nombre="IAE Salto",
                direccion="Misiones 192",
                telefono="47354602",
                email="iaesalto@gmail.com",
                logo="/logos/logoutu.png"
            )
            
            institucion3 = Institucion(
                nombre="Esc. Catalina H. de Castaños",
                direccion="Varela 440",
                telefono="47335987",
                email="ttssalto@gmail.com",
                logo="/logos/logoutu.png"
            )

            institucion4 = Institucion(
                nombre="Esc. De Administración",
                direccion="Juan C. Gomez 351",
                telefono="47323778",
                email="etays.salto@gmail.com",
                logo="/logos/logoutu.png"
            )

            institucion5 = Institucion(
                nombre="Esc. Agraria",
                direccion="Ruta a Salto Grande S/N",
                telefono="47322862",
                email="esagrariasalto@gmail.com",
                logo="/logos/logoutu.png"
            )
            
            instituciones_a_crear = [institucion1, institucion2, institucion3, institucion4, institucion5]
            session.add_all(instituciones_a_crear)
            print("✅ Instituciones preparadas para creación.")

            # 3. Crear los 5 Usuarios y vincularlos a las instituciones
            print("👥 Creando 5 usuarios y vinculándolos...")
            
            # Obtener contraseñas desde variables de entorno o usar la por defecto
            default_password = get_default_seed_password()
            
            usuario1 = Usuario(
                correo="cenur@cenur.com", 
                password_hash=hash_password(os.getenv("CENUR_PASSWORD", default_password)), 
                institucion=institucion1
            )
            usuario2 = Usuario(
                correo="iae@iae.com", 
                password_hash=hash_password(os.getenv("IAE_PASSWORD", default_password)), 
                institucion=institucion2
            )
            usuario3 = Usuario(
                correo="catalina@catalina.com", 
                password_hash=hash_password(os.getenv("CATALINA_PASSWORD", default_password)), 
                institucion=institucion3
            )
            usuario4 = Usuario(
                correo="administracion@administracion.com", 
                password_hash=hash_password(os.getenv("ADMINISTRACION_PASSWORD", default_password)), 
                institucion=institucion4
            )
            usuario5 = Usuario(
                correo="agraria@agraria.com", 
                password_hash=hash_password(os.getenv("AGRARIA_PASSWORD", default_password)), 
                institucion=institucion5
            )

            usuarios_a_crear = [usuario1, usuario2, usuario3, usuario4, usuario5]
            session.add_all(usuarios_a_crear)
            print("✅ Usuarios preparados para creación.")

            # 4. Guardar todo en la base de datos en una sola transacción
            session.commit()
            
            print("\n🎉 ¡Base de datos actualizada exitosamente!")
            print(f"📊 Se crearon {len(instituciones_a_crear)} instituciones y {len(usuarios_a_crear)} usuarios.")
            
            # Mostrar información de seguridad
            if default_password == "temporal_cambiar_2024!":
                print("\n⚠️  IMPORTANTE - SEGURIDAD:")
                print("   Los usuarios fueron creados con contraseñas temporales.")
                print("   En producción, cambia todas las contraseñas inmediatamente.")
                print("   Para usar contraseñas personalizadas, define estas variables de entorno:")
                print("   - DEFAULT_SEED_PASSWORD (contraseña general)")
                print("   - CENUR_PASSWORD, IAE_PASSWORD, CATALINA_PASSWORD, etc.")
            
            print("\n🔑 Usuarios creados:")
            for usuario in usuarios_a_crear:
                print(f"   📧 {usuario.correo} - Institución: {usuario.institucion.nombre}")
            
            return True
            
    except Exception as e:
        print(f"❌ Error durante el seed de la base de datos: {e}")
        return False

def poblar_cursos():
    # Diccionario: nombre de institución -> lista de cursos
    cursos_por_institucion = {
        "UDELAR – CENUR LN": [
            {"nombre": "Licenciatura en Informática", "nivel": "Universitario", "duracion_numero": "4", "duracion_unidad": "años", "requisitos_ingreso": "Bachillerato", "informacion": "Programa con fuerte énfasis en desarrollo de software y proyectos con clientes reales."},
            {"nombre": "Taller de Introducción a la Robótica", "nivel": "Terciario", "duracion_numero": "6", "duracion_unidad": "meses", "requisitos_ingreso": "Ciclo básico", "informacion": "Laboratorio con kits Arduino incluidos y participación en competencias locales."},
            {"nombre": "Diplomado en Ciencia de Datos", "nivel": "Posgrado", "duracion_numero": "12", "duracion_unidad": "meses", "requisitos_ingreso": "Universitario", "informacion": "Incluye prácticas en Python, R y uso de herramientas de Big Data."},
            {"nombre": "Curso Intensivo de Redes Cisco", "nivel": "Terciario", "duracion_numero": "3", "duracion_unidad": "meses", "requisitos_ingreso": "Bachillerato", "informacion": "Preparación para la certificación CCNA; clases 100 % prácticas."},
        ],
        "IAE Salto": [
            {"nombre": "Gestión de Emprendimientos", "nivel": "Terciario", "duracion_numero": "5", "duracion_unidad": "meses", "requisitos_ingreso": "Bachillerato", "informacion": "Plan de negocios y mentoría con incubadoras locales."},
            {"nombre": "Marketing Digital y E-Commerce", "nivel": "Terciario", "duracion_numero": "4", "duracion_unidad": "meses", "requisitos_ingreso": "Ciclo básico", "informacion": "Se trabaja con campañas reales en redes sociales y Google Ads."},
            {"nombre": "Tecnicatura en Administración", "nivel": "Bachillerato", "duracion_numero": "2", "duracion_unidad": "años", "requisitos_ingreso": "Ciclo básico", "informacion": "Prácticas profesionales en empresas de la zona."},
            {"nombre": "Curso de Contabilidad con Excel", "nivel": "Bachillerato", "duracion_numero": "2", "duracion_unidad": "meses", "requisitos_ingreso": "Ciclo básico", "informacion": "Incluye plantillas avanzadas y certificación interna."},
        ],
        "Esc. Catalina H. de Castaños": [
            {"nombre": "Electricidad Domiciliaria", "nivel": "Terciario", "duracion_numero": "4", "duracion_unidad": "meses", "requisitos_ingreso": "Ciclo básico", "informacion": "Prácticas en instalaciones reales y certificación oficial."},
            {"nombre": "Plomería y Gas", "nivel": "Terciario", "duracion_numero": "3", "duracion_unidad": "meses", "requisitos_ingreso": "Ciclo básico", "informacion": "Incluye materiales y herramientas de trabajo."},
            {"nombre": "Carpintería Básica", "nivel": "Terciario", "duracion_numero": "6", "duracion_unidad": "meses", "requisitos_ingreso": "Ciclo básico", "informacion": "Proyectos prácticos y venta de productos realizados."},
            {"nombre": "Mecánica Automotriz", "nivel": "Terciario", "duracion_numero": "8", "duracion_unidad": "meses", "requisitos_ingreso": "Ciclo básico", "informacion": "Taller propio con vehículos para prácticas."},
        ],
        "Esc. De Administración": [
            {"nombre": "Administración de Empresas", "nivel": "Bachillerato", "duracion_numero": "3", "duracion_unidad": "años", "requisitos_ingreso": "Ciclo básico", "informacion": "Formación integral en gestión empresarial."},
            {"nombre": "Contabilidad Básica", "nivel": "Terciario", "duracion_numero": "6", "duracion_unidad": "meses", "requisitos_ingreso": "Ciclo básico", "informacion": "Uso de software contable y prácticas en empresas."},
            {"nombre": "Secretariado Ejecutivo", "nivel": "Terciario", "duracion_numero": "2", "duracion_unidad": "años", "requisitos_ingreso": "Ciclo básico", "informacion": "Formación en herramientas de oficina y protocolo."},
            {"nombre": "Gestión de Recursos Humanos", "nivel": "Terciario", "duracion_numero": "1", "duracion_unidad": "año", "requisitos_ingreso": "Bachillerato", "informacion": "Prácticas en empresas y certificación en gestión de personal."},
        ],
        "Esc. Agraria": [
            {"nombre": "Técnico Agropecuario", "nivel": "Bachillerato", "duracion_numero": "3", "duracion_unidad": "años", "requisitos_ingreso": "Ciclo básico", "informacion": "Prácticas en campo y laboratorio propio."},
            {"nombre": "Horticultura Orgánica", "nivel": "Terciario", "duracion_numero": "8", "duracion_unidad": "meses", "requisitos_ingreso": "Ciclo básico", "informacion": "Invernadero experimental y venta de productos."},
            {"nombre": "Ganadería Intensiva", "nivel": "Terciario", "duracion_numero": "6", "duracion_unidad": "meses", "requisitos_ingreso": "Ciclo básico", "informacion": "Prácticas en tambo y granja modelo."},
            {"nombre": "Mecanización Agrícola", "nivel": "Terciario", "duracion_numero": "1", "duracion_unidad": "año", "requisitos_ingreso": "Ciclo básico", "informacion": "Taller de maquinaria agrícola y prácticas en campo."},
        ]
    }
    
    print("🎓 Poblando cursos para cada institución...")
    
    for nombre_inst, cursos in cursos_por_institucion.items():
        print(f"   📚 Agregando cursos para: {nombre_inst}")
        
        # Buscar la institución por nombre
        with Session(engine) as session:
            institucion = session.exec(
                select(Institucion).where(Institucion.nombre == nombre_inst)
            ).first()
            
            if not institucion:
                print(f"   ❌ Institución no encontrada: {nombre_inst}")
                continue
            
            # Agregar cada curso
            for curso_data in cursos:
                try:
                    # Normalizar unidad de duración
                    unidad = curso_data["duracion_unidad"].strip().lower()
                    if unidad in ["año", "años"]:
                        curso_data["duracion_unidad"] = "años"
                    elif unidad in ["mes", "meses"]:
                        curso_data["duracion_unidad"] = "meses"
                    # Agregar el ID de la institución al curso
                    curso_data["institucion_id"] = institucion.id
                    # Agregar el curso usando la función existente
                    agregar_curso(curso_data)
                    print(f"      ✅ {curso_data['nombre']}")
                except Exception as e:
                    print(f"      ❌ Error al agregar {curso_data['nombre']}: {e}")
    
    print("✅ Cursos poblados exitosamente.")

def poblar_base_de_datos():
    """
    Pobla la base de datos con datos iniciales, evitando duplicados.
    """
    with Session(engine) as session:
        print("🔧 Verificando y creando datos iniciales (seed)...")

        # --- 1. Crear Instituciones (si no existen) ---
        for data in INSTITUCIONES_DATA:
            institucion_existente = session.exec(select(Institucion).where(Institucion.nombre == data["nombre"])).one_or_none()
            if not institucion_existente:
                institucion = Institucion(**data)
                session.add(institucion)
                print(f"  -> Creada institución: {data['nombre']}")
        session.commit()
        print("✅ Instituciones verificadas/creadas.")

        # --- 2. Crear Usuarios (si no existen) ---
        for data in USUARIOS_DATA:
            usuario_existente = session.exec(select(Usuario).where(Usuario.correo == data["correo"])).one_or_none()
            if not usuario_existente:
                institucion = session.exec(select(Institucion).where(Institucion.nombre == data["institucion_nombre"])).one()
                hashed_password = bcrypt.hashpw(data["password"].encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                usuario = Usuario(
                    correo=data["correo"],
                    password_hash=hashed_password,
                    institucion_id=institucion.id
                )
                session.add(usuario)
                print(f"  -> Creado usuario: {data['correo']} para {institucion.nombre}")
        session.commit()
        print("✅ Usuarios verificados/creados.")
        
        # --- 3. Crear Cursos (si no existen) ---
        for nombre_institucion, cursos in CURSOS_POR_INSTITUCION.items():
            institucion = session.exec(select(Institucion).where(Institucion.nombre == nombre_institucion)).one_or_none()
            if not institucion:
                print(f"  ⚠️  No se encontró la institución '{nombre_institucion}' para agregar cursos.")
                continue

            print(f"📚 Agregando cursos para: {institucion.nombre}")
            for curso_data in cursos:
                curso_existente = session.exec(select(Curso).where(Curso.nombre == curso_data["nombre"], Curso.institucion_id == institucion.id)).one_or_none()
                if not curso_existente:
                    # Normalizar unidad
                    unidad = curso_data.get("duracion_unidad", "").strip().lower()
                    if unidad in ["año", "años"]:
                        curso_data["duracion_unidad"] = "años"
                    elif unidad in ["mes", "meses"]:
                        curso_data["duracion_unidad"] = "meses"

                    nuevo_curso = Curso(
                        nombre=curso_data["nombre"],
                        nivel=curso_data["nivel"],
                        duracion_numero=str(curso_data["duracion_numero"]),
                        duracion_unidad=curso_data["duracion_unidad"],
                        requisitos_ingreso=curso_data["requisitos_ingreso"],
                        info_adicional=curso_data.get("info_adicional"),
                        institucion_id=institucion.id
                    )
                    session.add(nuevo_curso)
                    print(f"  -> Creado curso: {curso_data['nombre']}")
        
        session.commit()
        print("✅ Cursos verificados/creados.")
        print("\n🎉 ¡Seed completado exitosamente!\n")

if __name__ == "__main__":
    success = seed_database()
    if success:
        print("\n✅ Seed completado exitosamente.")
        poblar_cursos()
        print("✅ Cursos de ejemplo precargados correctamente.")
        poblar_base_de_datos()
    else:
        print("\n❌ Seed falló. Revisa los errores anteriores.")
        exit(1)