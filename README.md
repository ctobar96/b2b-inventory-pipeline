# 📦 B2B Data Pipeline & Inventory Dashboard

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED.svg)
![AWS S3](https://img.shields.io/badge/AWS-S3-FF9900.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B.svg)

## 📌 Visión General
Este proyecto es una solución integral de ingeniería de datos (*End-to-End*) diseñada para la gestión operativa y financiera de **Comercializadora de Suministros Integrales SpA**. 

El sistema automatiza el procesamiento de ventas de inventario B2B, asegura el almacenamiento histórico en la nube y despliega métricas críticas de negocio (como ingresos netos y control de IVA mensual) en una interfaz interactiva de baja latencia.

## 🏗️ Arquitectura de Datos
El proyecto implementa un patrón de arquitectura moderna separando la capa de almacenamiento (Data Lake) de la capa de servicio, garantizando escalabilidad y alta disponibilidad.

1. **Extracción y Transformación (ETL):** Un pipeline en Python procesa y limpia los datos crudos de transacciones.
2. **Data Lake (AWS S3):** Los datos procesados se respaldan de manera inmutable en Amazon S3, asegurando un *Disaster Recovery* eficiente y un almacenamiento histórico de bajo costo.
3. **Capa de Servicio (PostgreSQL):** Los datos estructurados se ingestan en una base de datos relacional para permitir consultas analíticas rápidas y optimizadas.
4. **Visualización (Streamlit):** Un dashboard interactivo consume los datos directamente desde PostgreSQL, mostrando KPIs financieros y gráficos de distribución desarrollados con Plotly.

## 🛠️ Stack Tecnológico
* **Lenguaje Principal:** Python
* **Orquestación y Contenedores:** Docker & Docker Compose
* **Base de Datos:** PostgreSQL
* **Cloud Storage:** Boto3 (AWS S3)
* **Manipulación de Datos:** Pandas, SQLAlchemy, psycopg2
* **Frontend Analytics:** Streamlit, Plotly Express

## 🚀 Instalación y Ejecución Local
El entorno está completamente dockerizado, lo que elimina el problema de "en mi máquina sí funciona".

### Prerrequisitos
* Docker y Docker Compose instalados.
* Archivo `.env` configurado en la raíz del proyecto con las credenciales de AWS y variables de PostgreSQL (ver `.env.example`).

### Despliegue en 1 paso
Para levantar la base de datos y la aplicación web simultáneamente, ejecuta:
```bash
cd docker
docker compose up -d --build