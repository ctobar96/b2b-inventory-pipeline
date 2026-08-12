import os
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

def procesar_y_cargar_db(ruta_archivo_local):
    """
    Lee el archivo CSV crudo, valida los tipos de datos y lo inserta en PostgreSQL.
    """
    print(f"Iniciando procesamiento del archivo '{ruta_archivo_local}'...")

    try:
        # 1. Extracción local
        df = pd.read_csv(ruta_archivo_local)

        # 2. Limpieza y transformación de datos
        df['fecha_venta'] = pd.to_datetime(df['fecha_venta'], errors='coerce')  # Convertir a datetime

        # Filtro de Calidad: eliminaos cualquier registro que tena un total de 0 o negativo
        df =  df[df['total_clp'] > 0]

        # 3. Conexión a la Base de Datos PostgreSQL (Docker)
        # Leemos las credenciales desde tu .env de forma segura
        pg_user = os.getenv("POSTGRES_USER")
        pg_pass = os.getenv("POSTGRES_PASSWORD")    
        pg_db = os.getenv("POSTGRES_DB")
        pg_port = os.getenv("POSTGRES_PORT", '5432')


        # Formato: postgresql://usuario:contraseña@host:puerto/nombre_bd
        # Estas credenciales hacen match exacto con tu docker-compose.yml
        # Armamos el string de conexión dinámicamente asegurando que el host sea 'localhost'
        string_conexion = f"postgresql://{pg_user}:{pg_pass}@localhost:{pg_port}/{pg_db}"
        motor_db = create_engine(string_conexion)

        # 4. Carga de datos (Load) a la tabla 'ventas_procesadas'
        # if_exists='append' agrega las filas nuevas al final de la tabla si ya existe
        df.to_sql(name='ventas_procesadas', con=motor_db, if_exists='append', index=False)
        
        print("Transformación exitosa. Datos cargados en PostgreSQL.")
        return True
    
    except FileNotFoundError:
        print(f"Error: El archivo '{ruta_archivo_local}' no se encontró.")
        return False
    except pd.errors.EmptyDataError:
        print(f"Error: El archivo '{ruta_archivo_local}' está vacío.")
        return False
    except pd.errors.ParserError:
        print(f"Error: El archivo '{ruta_archivo_local}' tiene un formato incorrecto.")
        return False