import os
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from dotenv import load_dotenv

# Cargamos las variables ocultas desde el archivo .env
load_dotenv()

def subir_a_s3(ruta_archivo_local, nombre_bucket, ruta_en_s3):
    """
    Sube un archivo a un bucket de Amazon S3.

    Parámetros:
    - ruta_archivo_local: Ruta del archivo en el sistema local.
    - nombre_bucket: Nombre del bucket de S3.
    - ruta_en_s3: Ruta donde se almacenará el archivo en S3.

    Retorna:
    - True si la subida fue exitosa, False en caso contrario.
    """
    # Inicializamos el cliente s3
    # Boto3 leerá automátcamente las credenciales de tu archivo .env
    s3_client = boto3.client(
        's3',
        aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY'),
        region_name = os.getenv('AWS_REGION', 'us-east-1')  # Puedes cambiar la región según tus necesidades
    )

    print(f"Intentando subir '{ruta_archivo_local}' a 's3://{nombre_bucket}/{ruta_en_s3}'...")

    try:
        s3_client.upload_file(ruta_archivo_local, nombre_bucket, ruta_en_s3)
        print(f"Archivo '{ruta_archivo_local}' subido exitosamente a 's3://{nombre_bucket}/{ruta_en_s3}'.")
        return True
    
    except FileNotFoundError:
        print(f"Error: El archivo '{ruta_archivo_local}' no se encontró.")
        return False
    except NoCredentialsError:
        print("Error: No se encontraron credenciales de AWS. Asegúrate de que estén configuradas correctamente.")
        return False
    except ClientError as e:
        print(f"Error al subir el archivo a S3: {e}")
        return False