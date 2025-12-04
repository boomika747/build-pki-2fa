from fastapi import FastAPI
from totp_utils import generate_totp_code, verify_totp_code

app = FastAPI()

SEED_FILE = "/data/seed.txt"   # <-- Correct path inside container

@app.get("/")
def home():
    return {"status": "ok"}

@app.get("/generate-2fa")
def generate_2fa():
    with open(SEED_FILE, "r") as f:
        hex_seed = f.read().strip()

    code = generate_totp_code(hex_seed)
    return {"code": code, "valid_for": 30}

@app.post("/verify-2fa/{user_code}")
def verify_2fa(user_code: str):
    with open(SEED_FILE, "r") as f:
        hex_seed = f.read().strip()

    result = verify_totp_code(hex_seed, user_code)
    return {"valid": result}


