import requests
import pandas as pd
import random
import uuid
from datetime import datetime

# ==========================================
# 1. FUNCIÓN PARA EXTRAER LA UF DESDE LA API
# ==========================================
def obtener_uf_daria():
    url ="https://mindicador.cl/api/uf"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Lanza una excepción si la respuesta no es exitosa
        data = response.json()

        # Extraemos el valor del primer registro (el más reciente)
        valor_uf_hoy = data['serie'][0]['valor']
        return valor_uf_hoy
    except Exception as e:
        print(f"Error al obtener la UF: {e}")
        return None

# ==========================================
# 2. FUNCIÓN PARA GENERAR INVENTARIO Y VENTAS
# ==========================================
def generar_ventas_b2b(num_registros=50, valor_uf=None):
    #Catálogo de productos enfocado en tu rubro comercial
    catalogo = [
        {"sku": "EPP-GLV-NIT", "nombre": "Guantes de Nitrilo (Caja x100)", "precio_neto": 8500},
        {"sku": "EPP-GLV-LTH", "nombre": "Guantes de Cuero Mosquetero", "precio_neto": 3800},
        {"sku": "EPP-HLM-SFT", "nombre": "Casco de Seguridad Industrial", "precio_neto": 4500},
        {"sku": "HDW-TIE-PL", "nombre": "Amarras Plásticas 30cm (Bolsa x100)", "precio_neto": 2200}
    ]

    ventas = []
    fecha_hoy = datetime.now().strftime("%Y-%m-%d")

    for _ in range(num_registros):
        producto = random.choice(catalogo)
        cantidad = random.randint(5, 50) # Simulamos compras por volumen (B2B)

        # Lógica de facturación
        subtotal = producto["precio_neto"] * cantidad
        iva = subtotal * 0.19  # IVA del 19%
        total_clp= subtotal + iva

        # Conversión a UF si la Api respondió correctamente
        total_uf = total_clp / valor_uf if valor_uf else None

        ventas.append({
            "id_transaccion": f"TRX-{str(uuid.uuid4())[:8].upper()}",
            "fecha_venta": fecha_hoy,
            "sku": producto["sku"],
            "producto": producto["nombre"],
            "cantidad_vendida": cantidad,
            "precio_unitario_neto": producto["precio_neto"],
            "subtotal_clp": subtotal,
            "iva_clp": iva,
            "total_clp": total_clp,
            "valor_uf_dia": valor_uf,
            "total_uf": total_uf
        })

        # Convertimos a lista a diccionario en un DataFrame de pandas
    df_ventas = pd.DataFrame(ventas)
    return df_ventas

# ==========================================
# 3. EJECUCIÓN PRINCIPAL DEL PIPELINE FASE 1
# ==========================================
if __name__ == "__main__":
    print("Iniciando la generación de datos de ventas B2B")

    #Paso 1: Obtener UF
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
    df.to_csv(nombre_archivo, index=False)

    print(f"✅ Proceso finalizado. Archivo generado: {nombre_archivo}")
    print("\nVista previa de los datos:")
    print(df[['id_transaccion', 'producto', 'total_clp', 'total_uf']].head())
