# Usar una imagen base de Python
FROM python:3.12-slim

# Instalar dependencias
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

#instalar certificados CA necesarios
RUN apt-get update && apt-get install -y ca-certificates

# Copiar código de la aplicación
COPY . /app
WORKDIR /app

# Exponer el puerto en el que se ejecutará la aplicación
EXPOSE 8000

# Comando para iniciar la aplicación
CMD ["python", "ApiConsumo.py"]
