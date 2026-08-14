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
    
    string_conexion = f"postgresql://{pg_user}:{pg_pass}@postgres:{pg_port}/{pg_db}"
    motor_db = create_engine(string_conexion)
    
    query = "SELECT * FROM ventas_procesadas"
    return pd.read_sql(query, motor_db)