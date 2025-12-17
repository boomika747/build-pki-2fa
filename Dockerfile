FROM python:3.10-slim

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    cron \
    tzdata \
    && rm -rf /var/lib/apt/lists/*

# Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . /app

ENV PYTHONPATH=/app
ENV TZ=UTC

# Cron setup
RUN chmod +x /app/cron/log_2fa_cron.py && crontab /app/cron/2fa-cron

EXPOSE 8080

CMD cron && uvicorn app:app --host 0.0.0.0 --port 8080
