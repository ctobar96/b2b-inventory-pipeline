import os
from datetime import datetime
from dotenv import load_dotenv

# Importarmos los módulos de extracción y carga
from src.extract.generador_b2b import generar_ventas_b2b, obtener_uf_daria
from src.load.s3_uploader import subir_a_s3
from src.transform.data_cleaner import procesar_y_cargar_db

# Cargamos las variables ocultas desde el archivo .env
load_dotenv()

def ejecutar_pipeline():
    print("Iniciando Pipeline de Inteligencia de Inventario B2B")

    # ==============================================================================================================================
    # FASE 1: EXTRACCIÓN Y GENERACIÓN
    # ==============================================================================================================================
    print("--> Fase 1: Extracción y Generación de Datos")

    uf_hoy = obtener_uf_daria()
    if uf_hoy:
        print(f"Valor de la UF hoy: {uf_hoy}")
    else:
        print("No se pudo obtener el valor de la UF. Se continuará sin conversión a UF.")

    # Paso 2: Generar datos sinteticos de ventas B2B
    print("Generando datos de ventas e inventario")
    df = generar_ventas_b2b(num_registros=100, valor_uf=uf_hoy)

    # Paso 3: Exportar a CSV
    nombre_archivo = f"ventas_b2b_raw_{datetime.now().strftime('%Y%m%d')}.csv"

    # Definir la ruta para guardar el archivo en la carpeta 'data/raw'
    ruta_carpeta = os.path.join("data", "raw")

    # En el caso de que no exita la carpeta la creamos
    os.makedirs(ruta_carpeta, exist_ok=True)

    # unimos la carpeta con el nombre del archivo para obtener la ruta completa
    ruta_completa = os.path.join(ruta_carpeta, nombre_archivo)

    df.to_csv(ruta_completa, index=False)

    print(f"✅ Proceso finalizado. Archivo generado: {nombre_archivo}")
    print(f"Archivo guardado en: {ruta_completa}")
    print("\nVista previa de los datos:")
    print(df[['id_transaccion', 'producto', 'total_clp', 'total_uf']].head())
    print() # Salto de línea estético

    # ==============================================================================================================================
    # FASE 2: CARGA A S3    
    # ==============================================================================================================================
    print("--> Fase 2: Cargar a la Nube (AWS)")

    # lee el nombre del bucket desde el archivo .env
    bucket_destino = os.getenv("S3_BUCKET_NAME")

    if not bucket_destino:
        print("Error: No se encontró el Bucket S3_BICKET_NAME en el archivo .env")
        return

    # Definir el nombre del archivo en S3
    ruta_s3= f"raw/{nombre_archivo}"

    # Llamamos a la función para subir el archivo a S3
    subida_exitosa = subir_a_s3(ruta_completa, bucket_destino, ruta_s3)

    print() # Salto de línea estético
    
    # ==============================================================================================================================
    # FASE 2: CARGA A S3    
    # ==============================================================================================================================
    print("--> FASE 3: Transformación y Carga a Base de Datos (PostgreSQL)")

    # Llamamos a la función para procesar y cargar los datos a PostgreSQL
    carga_db_exitosa = procesar_y_cargar_db(ruta_completa)

    # Resumen Final
    print("\n==================== RESUMEN FINAL ====================")
    if carga_db_exitosa and subida_exitosa:
        print("✅ Pipeline completado exitosamente. Datos generados, subidos a S3 y cargados en PostgreSQL.")
    elif not carga_db_exitosa and subida_exitosa:
        print("⚠️ Pipeline completado parcialmente. Datos subidos a S3, pero hubo un error al cargar en PostgreSQL.")
    elif carga_db_exitosa and not subida_exitosa:
        print("⚠️ Pipeline completado parcialmente. Datos cargados en PostgreSQL, pero hubo un error al subir a S3.")
    else:
        print("❌ Pipeline fallido. Hubo errores tanto al subir a S3 como al cargar en PostgreSQL.")


if __name__ == "__main__":
    ejecutar_pipeline()