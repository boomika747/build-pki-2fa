FROM python:3.10-slim

WORKDIR /app

# ----------------------------
# System dependencies
# ----------------------------
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    cron \
    tzdata \
    && rm -rf /var/lib/apt/lists/*

# ----------------------------
# Python dependencies
# ----------------------------
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# ----------------------------
# Copy application
# ----------------------------
COPY . /app

# ----------------------------
# Environment
# ----------------------------
ENV PYTHONPATH=/app
ENV TZ=UTC

# ----------------------------
# IMPORTANT FIXES
# ----------------------------

# 1️⃣ Ensure /data exists (cron + seed storage)
RUN mkdir -p /data

# 2️⃣ Make cron script executable
RUN chmod +x /app/cron/log_2fa_cron.py

# 3️⃣ Install cron job
RUN crontab /app/cron/2fa-cron

# ----------------------------
# Expose API
# ----------------------------
EXPOSE 8080

# ----------------------------
# Start cron + API
# ----------------------------
CMD cron && uvicorn app:app --host 0.0.0.0 --port 8080
