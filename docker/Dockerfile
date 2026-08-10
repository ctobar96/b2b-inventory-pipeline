FROM python:3.12-slim

# Dependencias del sistema necesarias para PostgreSQL
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Directorio de trabajo
WORKDIR /app

# Instalar dependencias Python
COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copiar proyecto
COPY . .

# Puerto de Streamlit
EXPOSE 8501

# Ejecutar aplicación
CMD ["streamlit", "run", "dashboards/app_streamlit.py", "--server.address=0.0.0.0"]
