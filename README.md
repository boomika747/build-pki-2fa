PKI-Based 2FA Microservice (Dockerized)
Overview

This project implements a secure Two-Factor Authentication (2FA) microservice using FastAPI, Time-based One-Time Passwords (TOTP), Public Key Infrastructure (PKI), Docker, and cron automation.
It demonstrates secure seed handling, cryptographic integrity verification, containerized deployment, and automated background tasks.

Features

Secure seed generation and persistent storage

PKI-based Git commit integrity verification

RFC-compliant TOTP generation

2FA verification API

Fully Dockerized application

Automated cron job for periodic 2FA logging

Persistent data storage using Docker volumes

Technology Stack
Category	Technology
Language	Python 3.10
Framework	FastAPI
Security	OpenSSL (PKI)
OTP	TOTP (RFC-compliant)
Hashing	SHA-256
Containerization	Docker, Docker Compose
Scheduler	Linux Cron
Project Structure
build-pki-2fa/
│
├── app.py
├── totp_utils.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
│
├── student_private.pem
├── student_public.pem
├── commit_hash.txt
├── commit_proof.sig
│
├── cron/
│   ├── log_2fa_cron.py
│   └── 2fa-cron
│
└── data/
    ├── seed.txt
    └── last_code.txt

Setup and Execution
Step 1: Clone the Repository
git clone <your-repo-url>
cd build-pki-2fa

Step 2: Verify Git Commit Integrity Using PKI
git rev-parse HEAD > commit_hash.txt
openssl dgst -sha256 -sign student_private.pem commit_hash.txt > commit_proof.sig
openssl dgst -sha256 -verify student_public.pem \
  -signature commit_proof.sig commit_hash.txt


Expected output:

Verified OK

Step 3: Build Docker Image
docker compose build --no-cache

Step 4: Start the Application
docker compose up -d


Verify running containers:

docker ps

API Endpoints
Health Check
curl http://localhost:8080/


Response:

{"status":"ok"}

Generate 2FA Code
curl http://localhost:8080/generate-2fa


Response:

{"code":"436634","valid_for":30}

Verify Valid 2FA Code
curl -X POST http://localhost:8080/verify-2fa \
-H "Content-Type: application/json" \
-d '{"code":"436634"}'


Response:

{"valid":true}

Verify Invalid 2FA Code
curl -X POST http://localhost:8080/verify-2fa \
-H "Content-Type: application/json" \
-d '{"code":"000000"}'


Response:

{"valid":false}

Seed Verification Inside Container
docker exec -it build-pki-2fa-app sh -c "ls -l /data && cat /data/seed.txt"


This confirms that the seed is securely stored and persistent.

Cron Job Verification

Check cron entry:

docker exec -it build-pki-2fa-app crontab -l


Expected output:

* * * * * /usr/local/bin/python3 /app/cron/log_2fa_cron.py


View logged 2FA codes:

docker exec -it build-pki-2fa-app sh -c "tail -5 /data/last_code.txt"


Example output:

2025-12-18 13:39:01 2FA Code: 700383
2025-12-18 13:40:01 2FA Code: 517025

Security Considerations

The TOTP seed is never exposed via public APIs

Commit authenticity is verified using PKI signatures

SHA-256 is used for hashing operations

TOTP codes are time-bound and expire automatically

Application runs in an isolated Docker environment

Final Status

All APIs are functional

PKI verification completed successfully

Cron automation verified

Docker build is reproducible

Secure seed storage confirmed

Conclusion

This project provides a secure and reliable implementation of a PKI-verified 2FA microservice using modern containerization and cryptographic practices.
It is suitable for academic evaluation and demonstrates real-world security design principles.