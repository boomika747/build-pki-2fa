from fastapi import FastAPI, HTTPException, Request
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
async def decrypt_seed(request: Request):
    body = await request.body()
    data = None
    try:
        data = await request.json()
        encrypted_seed_b64 = data.get("encrypted_seed", "") or data.get("seed", "") or data.get("data", "")
    except Exception:
        encrypted_seed_b64 = body.decode('utf-8')
    
    if not encrypted_seed_b64 and isinstance(data, str):
        encrypted_seed_b64 = data
        
    return decrypt_seed_route(encrypted_seed_b64)

@app.get("/generate-2fa")
def generate_2fa():
    try:
        with open(SEED_FILE, "r") as f:
            seed = f.read().strip()
    except FileNotFoundError:
        raise HTTPException(500, "Seed not found")

    code = generate_totp_code(seed)
    
    import time
    valid_for = 30 - (int(time.time()) % 30)

    with open("/data/last_code.txt", "w") as f:
        f.write(code)

    return {"code": code, "valid_for": valid_for}

class CodeRequest(BaseModel):
    code: str

@app.post("/verify-2fa")
def verify_2fa(req: CodeRequest):
    if not os.path.exists(SEED_FILE):
        raise HTTPException(400, "Seed not found")

    with open(SEED_FILE) as f:
        seed = f.read().strip()

    is_valid = verify_totp_code(seed, req.code)
    return {"valid": is_valid}
