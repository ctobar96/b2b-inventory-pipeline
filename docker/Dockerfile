FROM python:3.12-slim

# Evitar archivos .pyc y mantener logs visibles
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Dependencias del sistema necesarias para PostgreSQL
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       gcc \
       libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependencias Python
COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copiar proyecto
COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "dashboards/app_streamlit.py", "--server.address=0.0.0.0"]
