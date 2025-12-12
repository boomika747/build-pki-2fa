from fastapi import FastAPI, HTTPException
from totp_utils import generate_totp_code, verify_totp_code
from decrypt_seed import decrypt_seed_route
import os
import secrets

app = FastAPI()

SEED_FILE = "/data/seed.txt"        # persistent seed storage
ENCRYPTED_SEED = "/encrypted_seed.txt"


@app.get("/")
def home():
    return {"status": "ok"}


# 1. Request seed (create seed if missing)
@app.get("/request-seed")
def request_seed():
    # If seed does NOT exist -> create one
    if not os.path.exists(SEED_FILE):
        seed = secrets.token_hex(32)  # 64-char hex
        with open(SEED_FILE, "w") as f:
            f.write(seed)

    # Load the seed
    with open(SEED_FILE, "r") as f:
        seed_hex = f.read().strip()

    return {"seed": seed_hex}


# 2. Decrypt instructor seed -> save to /data/seed.txt
@app.post("/decrypt-seed")
def decrypt_seed():
    # This should read encrypted_seed.txt and keys, then write the hex seed to SEED_FILE
    return decrypt_seed_route()


# 3. Generate a TOTP using the stored seed
@app.get("/generate-2fa")
def generate_2fa():
    if not os.path.exists(SEED_FILE):
        raise HTTPException(
            status_code=400,
            detail="Seed not found. Call /request-seed or /decrypt-seed first.",
        )

    with open(SEED_FILE, "r") as f:
        hex_seed = f.read().strip()

    code = generate_totp_code(hex_seed)
    return {"code": code, "valid_for": 30}


# 4. Verify the TOTP entered by user
@app.post("/verify-2fa/{user_code}")
def verify_2fa(user_code: str):
    if not os.path.exists(SEED_FILE):
        raise HTTPException(
            status_code=400,
            detail="Seed not found. Call /request-seed or /decrypt-seed first.",
        )

    with open(SEED_FILE, "r") as f:
        hex_seed = f.read().strip()

    result = verify_totp_code(hex_seed, user_code)
    return {"valid": result}
