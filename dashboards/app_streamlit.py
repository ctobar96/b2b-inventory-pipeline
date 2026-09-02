import sys
import os

# 1. Le decimos a Python que busque módulos en la carpeta principal (un nivel arriba)
ruta_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(ruta_raiz)


import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px

from src.api import obtener_ventas_procesadas


# Configuracion de la pagina 
st.set_page_config(page_title="Dashboard Inventario", layout="wide")

st.title("Panel de Control B2B")
st.subheader("Comercializadora de Suministros integrales SpA")
st.markdown("---")

# 1. Conectamos la fución externa con el caché de Streamlit
@st.cache_data
def cargar_datos():
    return obtener_ventas_procesadas()

try:
    df =  cargar_datos()

    # 2. Tarjetas de KPIs principales
    col1, col2, col3 = st.columns(3)

    total_ventas = df['total_clp'].sum()
    total_iva = df['iva_clp'].sum()
    unidades_vendidas = df['cantidad_vendida'].sum()

    col1.metric("Ingresos Totales (CLP)", f"${total_ventas:,.0f}")
    col2.metric("Control IVA mensual", f"${total_iva:,.0f}")
    col3.metric("Unidades Salientes", f"{unidades_vendidas:,}")

    st.markdown("---")

    # 3. Gráficos Interactivos
    col_chart1, col_chart2 =  st.columns(2)

    with col_chart1:
        st.write("### inventario Saliente por Producto")
        df_agrupado = df.groupby('producto')['cantidad_vendida'].sum().reset_index()
        fig1 = px.bar(df_agrupado, x='producto', y='cantidad_vendida', color='producto')
        st.plotly_chart(fig1, use_container_width=True)

    with col_chart2:
        st.write("### Distribución de Ingresos Netos")
        df_ingresos = df.groupby('producto')['subtotal_clp'].sum().reset_index()
        fig2 = px.pie(df_ingresos, values='subtotal_clp', names='producto', hole=0.4)
        st.plotly_chart(fig2, use_container_width=True)

    # 4. Tabla de datos crudos
    st.write("### Registro de Transacciones")
    st.dataframe(df)

except Exception as e:
    st.error(f"Error al conectar con la base de datos: {e}")