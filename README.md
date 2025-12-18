🔐 PKI-Based 2FA Microservice (Dockerized)

This project implements a PKI-secured Two-Factor Authentication (2FA) microservice using FastAPI, TOTP, OpenSSL, Docker, and Cron automation.
It demonstrates secure seed handling, digital signature verification, containerization, and scheduled background tasks.

📌 Features

🔑 Secure seed generation and storage

🔐 PKI-based commit integrity verification

🔢 Time-based One-Time Password (TOTP) generation

✅ 2FA code verification API

🐳 Fully Dockerized application

⏱ Automated cron job for logging 2FA codes

📁 Persistent secure data storage

🛠️ Tech Stack

Language: Python 3.10

Framework: FastAPI

Security: OpenSSL (PKI)

Containerization: Docker & Docker Compose

Scheduler: Linux Cron

Hashing: SHA-256

OTP: RFC-compliant TOTP

📂 Project Structure
build-pki-2fa/
│
├── app.py
├── totp_utils.py
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
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

🚀 Setup & Execution
1️⃣ Clone Repository
git clone <your-repo-url>
cd build-pki-2fa

2️⃣ Verify Git Commit Integrity (PKI)
git rev-parse HEAD > commit_hash.txt
openssl dgst -sha256 -sign student_private.pem commit_hash.txt > commit_proof.sig
openssl dgst -sha256 -verify student_public.pem \
-signature commit_proof.sig commit_hash.txt


✅ Expected Output:

Verified OK

3️⃣ Build Docker Image (No Cache)
docker compose build --no-cache

4️⃣ Start Application
docker compose up -d


Verify:

docker ps

🌐 API Endpoints
🔍 Health Check
curl http://localhost:8080/


Response:

{"status":"ok"}

🔢 Generate 2FA Code
curl http://localhost:8080/generate-2fa


Response:

{"code":"436634","valid_for":30}

✅ Verify Valid Code
curl -X POST http://localhost:8080/verify-2fa \
-H "Content-Type: application/json" \
-d '{"code":"436634"}'


Response:

{"valid":true}

❌ Verify Invalid Code
curl -X POST http://localhost:8080/verify-2fa \
-H "Content-Type: application/json" \
-d '{"code":"000000"}'


Response:

{"valid":false}

📁 Seed Verification (Inside Container)
docker exec -it build-pki-2fa-app sh -c "ls -l /data && cat /data/seed.txt"


✔ Seed is securely stored and persistent.

⏱ Cron Job Verification
Check Cron Entry
docker exec -it build-pki-2fa-app crontab -l


Expected:

* * * * * /usr/local/bin/python3 /app/cron/log_2fa_cron.py

View Logged 2FA Codes
docker exec -it build-pki-2fa-app sh -c "tail -5 /data/last_code.txt"


Example Output:

2025-12-18 13:39:01 2FA Code: 700383
2025-12-18 13:40:01 2FA Code: 517025

🔐 Security Highlights

Seed never exposed publicly

PKI verifies commit authenticity

SHA-256 hashing

TOTP time-bound validity

Isolated Docker runtime

✅ Final Status

✔ All APIs functional
✔ PKI verification successful
✔ Cron automation working
✔ Docker build reproducible
✔ Secure seed storage confirmed

🏁 Conclusion

This project demonstrates a production-ready secure 2FA microservice with cryptographic verification, containerization, and automated background execution.