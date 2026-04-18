#!/bin/bash
echo "--- Iniciando Despliegue ---"

# 1. Bajamos los cambios (Asegúrate de estar en la carpeta correcta)
# Como el volumen está en /app, entramos ahí
cd /app

git pull origin Carlos

echo "--- Reconstruyendo Contenedores ---"
# Usamos 'compose' (sin el guion si usas la versión nueva de Docker)
docker compose up -d --build