FROM python:3.12-slim

WORKDIR /app

# Dépendances système
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier dans /app/server/ pour que "server.interfaces.main" resolve correctement
COPY . ./server/

# PYTHONPATH=/app => "import server.xxx" => /app/server/xxx
ENV PYTHONPATH=/app

EXPOSE 8000
