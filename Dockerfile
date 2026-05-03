FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip uninstall -y google-generativeai google-api-core google-auth google-cloud-core
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD ["python", "-m", "bot.main"]
