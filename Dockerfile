FROM python:3.11-slim

# Instalar dependencias del sistema (si mathml2docx necesita lxml, etc.)
RUN apt-get update && apt-get install -y \
    libxml2 \
    libxslt1.1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

# Gunicorn como servidor WSGI
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "main:app"]
