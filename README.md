# b2b-inventory-pipeline

# B2B Inventory Pipeline

## 📌 Descripción

Pipeline de datos para la gestión y análisis de inventario B2B.

B2B Inventory Data Pipeline — Diseño e implementación de un pipeline de datos utilizando Python, PostgreSQL, Docker y Amazon S3, con dashboards interactivos desarrollados en Streamlit y Power BI para análisis de inventario y métricas de negocio.

Python | SQL | PostgreSQL | Docker | AWS S3 |
Streamlit | Power BI | Pandas | Git

## 🏗️ Arquitectura

[imagen de arquitectura]

## 🛠️ Tecnologías

- Python
- Pandas
- PostgreSQL
- Docker
- Amazon S3
- Streamlit
- Power BI
- SQL
- AWS

## 📊 Dashboards

### Streamlit

[imagen]

### Power BI

[imagen]

## 🚀 Ejecución

### 1. Clonar repositorio

git clone ...

### 2. Crear entorno virtual

python -m venv .venv

### 3. Instalar dependencias

pip install -r requirements.txt

### 4. Configurar variables

cp .env.example .env

### 5. Levantar PostgreSQL

docker compose -f docker/docker-compose.yml up -d postgres

### 6. Ejecutar Streamlit

streamlit run dashboards/app_streamlit.py



| Variable            | Significado                          | Tu valor           |
| ------------------- | ------------------------------------ | ------------------ |
| `POSTGRES_USER`     | Usuario de PostgreSQL                | `admin_datos`      |
| `POSTGRES_PASSWORD` | Contraseña del usuario               | `superpassword123` |
| `POSTGRES_DB`       | Base de datos inicial                | `b2b_analytics`    |
| `POSTGRES_PORT`     | Puerto expuesto en tu máquina        | `5432`             |
| `POSTGRES_HOST`     | Nombre del servidor dentro de Docker | `postgres`         |



Para evitar esto y enfocarnos solo en la Fase 3, le diremos a Docker que levante exclusivamente el servicio de la base de datos.Sigue esta secuencia exacta en tu terminal:1.Inicia PostgreSQL:Levantar solo la base de datos.Primero, entra a la carpeta de Docker y levanta específicamente el servicio postgres en segundo plano (con la bandera -d):Bashcd docker
docker-compose up -d postgres
Nota: Verás que dice "Started b2b_postgres". Docker descargará la imagen (si no la tiene) y la encenderá en segundos.2.Vuelve a la raíz del proyecto:Asegurar la ruta de ejecución.Tu orquestador principal debe ejecutarse siempre desde la carpeta principal del proyecto, así que retrocede un nivel:Bashcd ..
3.Ejecuta tu Orquestador E2E:La prueba de fuego.Ahora sí, con la base de datos esperando conexiones, lanza el pipeline completo:Bashpython -m src.main
Si toda la configuración es correcta, verás en tu terminal cómo los datos se extraen (Fase 1), se aseguran en tu Data Lake de Amazon S3 (Fase 2) y, finalmente, se limpian y se inyectan en tu base de datos local en Docker (Fase 3), finalizando con el mensaje 🎉 PIPELINE E2E COMPLETADO EXITOSAMENTE.


| Componente     | ¿Dónde vive?                        | ¿Tiene costo?           | Función                                                     |
| -------------- | ----------------------------------- | ----------------------- | ----------------------------------------------------------- |
| **Amazon S3**  | En la nube pública (AWS - Virginia) | Pago por uso (céntimos) | Bóveda de almacenamiento histórico a largo plazo.           |
| **PostgreSQL** | En tu computador local (Docker)     | Gratis                  | Motor analítico rápido para consultar el inventario actual. |
