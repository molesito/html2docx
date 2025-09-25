FROM pandoc/core:latest

# Instalar python + flask + gunicorn
RUN apk add --no-cache python3 py3-pip
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "main:app"]
