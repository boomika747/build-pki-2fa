from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from totp_utils import generate_totp_code, verify_totp_code
from decrypt_seed import decrypt_seed_route
import os, secrets

app = FastAPI()

SEED_FILE = "/data/seed.txt"

@app.get("/")
def home():
    return {"status": "ok"}

@app.get("/request-seed")
def request_seed():
    if not os.path.exists(SEED_FILE):
        seed = secrets.token_hex(32)
        os.makedirs("/data", exist_ok=True)
        with open(SEED_FILE, "w") as f:
            f.write(seed)

    with open(SEED_FILE) as f:
        return {"seed": f.read().strip()}

@app.post("/decrypt-seed")
def decrypt_seed():
    return decrypt_seed_route()

@app.get("/generate-2fa")
def generate_2fa():
    with open(SEED_FILE, "r") as f:
        seed = f.read().strip()

    code = generate_totp_code(seed)

    # 🔴 THIS LINE WAS MISSING / WRONG
    with open("/data/last_code.txt", "w") as f:
        f.write(code)

    return {"code": code, "valid_for": 30}

class CodeRequest(BaseModel):
    code: str

@app.post("/verify-2fa")
def verify_2fa(req: CodeRequest):
    if not os.path.exists(SEED_FILE):
        raise HTTPException(400, "Seed not found")

    with open(SEED_FILE) as f:
        seed = f.read().strip()

    return {"valid": verify_totp_code(seed, req.code)}
