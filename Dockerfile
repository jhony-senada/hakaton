FROM python:3.11-slim

# Instalamos git y dependencias para poder instalar Docker CLI
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && curl -fsSL https://get.docker.com | sh \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000
CMD ["python", "app.py"]