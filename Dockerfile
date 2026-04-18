# Usa una imagen oficial y ligera de Python
FROM python:3.11-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia primero los requerimientos para aprovechar el caché de Docker
COPY requirements.txt .

# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copia el resto del código de tu proyecto al contenedor
COPY . .

# Expone el puerto 5000 que utiliza Flask
EXPOSE 5000

# Comando para iniciar la aplicación
CMD ["python", "app.py"]