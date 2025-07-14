from sqlmodel import SQLModel, create_engine
import os

# Usar la misma ruta que el proyecto
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/saltoestudia.db")
engine = create_engine(DATABASE_URL)

from saltoestudia.models import *  # Importa todos los modelos

print(f"Creando todas las tablas en {DATABASE_URL} ...")
SQLModel.metadata.create_all(engine)
print("¡Listo!") 