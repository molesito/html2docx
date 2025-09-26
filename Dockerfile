FROM python:3.11-slim

# Instalar dependencias de sistema y pandoc
RUN apt-get update && apt-get install -y pandoc && rm -rf /var/lib/apt/lists/*

# Crear directorio
WORKDIR /app

# Instalar requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY main.py .

# Exponer puerto
EXPOSE 8000

# Comando de ejecución
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
