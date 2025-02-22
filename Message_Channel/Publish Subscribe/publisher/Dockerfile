FROM python:3.9
WORKDIR /app

# Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente
COPY . .

CMD ["python", "publisher.py"]  # Para publisher
# Para subscriber, cambiar a "subscriber.py"
