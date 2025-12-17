import base64, os
from fastapi import HTTPException
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes

SEED_FILE = "/data/seed.txt"
ENCRYPTED_SEED = "/app/encrypted_seed.txt"
PRIVATE_KEY = "/app/student_private.pem"

def decrypt_seed_route():
    try:
        with open(ENCRYPTED_SEED) as f:
            encrypted = base64.b64decode(f.read().strip())

        with open(PRIVATE_KEY, "rb") as f:
            private_key = serialization.load_pem_private_key(f.read(), None)

        seed = private_key.decrypt(
            encrypted,
            padding.OAEP(
                mgf=padding.MGF1(hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        ).decode()

        if len(seed) != 64:
            raise ValueError("Invalid seed")

        os.makedirs("/data", exist_ok=True)
        with open(SEED_FILE, "w") as f:
            f.write(seed)

        return {"status": "success"}

    except Exception as e:
        raise HTTPException(500, str(e))
