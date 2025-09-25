FROM pandoc/core:latest

# Instalar Python 3 y pip
RUN apk add --no-cache python3 py3-pip

# Crear y activar un virtualenv en /opt/venv
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Crear carpeta de la app
WORKDIR /app

# Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código
COPY main.py .

# Lanzar con gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "main:app"]
