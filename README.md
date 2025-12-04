# PKI 2FA Microservice
PKI-Based TOTP 2FA Microservice

This project implements a secure Two-Factor Authentication (2FA) service using Public Key Infrastructure (PKI) and Time-based One-Time Passwords (TOTP).

Features

Secure TOTP seed encryption using RSA keys

Generate valid 6-digit OTPs every 30 seconds

Verify OTP through API

Cron job to log OTP automatically

Fully containerized using Docker

Project Structure
app.py                # FastAPI service
scripts/              # OTP generation, verification, cron scripts
student_public.pem    # Your public key
instructor_public.pem # Instructor's public key
data/                 # Stores decrypted seed (volume)
logs/                 # Cron logs (volume)
Dockerfile
docker-compose.yml

Run the Service
docker-compose up --build


API runs at:

http://127.0.0.1:8000/

Endpoints

GET /generate-2fa → Generate OTP

POST /verify-2fa → Verify OTP

Note

Sensitive files like private keys and seed scripts are not included in the repo for security reasons.