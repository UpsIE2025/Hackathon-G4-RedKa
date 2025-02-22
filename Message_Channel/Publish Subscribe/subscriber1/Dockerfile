# Usa una imagen base de Python
FROM python:3.9

# Establecer el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar los archivos necesarios
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . .

# Asegurar que python3 esté disponible como python
RUN ln -s /usr/bin/python3 /usr/bin/python

# Ejecutar el subscriber con FastAPI
CMD ["uvicorn", "subscriber:app", "--host", "0.0.0.0", "--port", "8001"]
