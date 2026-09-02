import pandas as pd
from sqlalchemy import create_engine
import os

def obtener_ventas_procesadas():
    """
    Se conecta a PostgreSQL y extrae el dataframe completo de ventas.
    """

    pg_user = os.getenv('POSTGRES_USER')
    pg_pass = os.getenv('POSTGRES_PASSWORD')
    pg_db = os.getenv('POSTGRES_DB')
    pg_port = os.getenv('POSTGRES_PORT', '5432')
    
    # Buscamos el host en las variables de entorno. 
    # Si no existe, usamos 'b2b_postgres' (el nombre de tu contenedor) por defecto.
    pg_host = os.getenv('DB_HOST', 'b2b_postgres')
    
    # Inyectamos pg_host en lugar de la palabra fija
    string_conexion = f"postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}"
    motor_db = create_engine(string_conexion)
    
    query = "SELECT * FROM ventas_procesadas"
    return pd.read_sql(query, motor_db)