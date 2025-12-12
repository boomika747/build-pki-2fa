import base64
from fastapi import HTTPException
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes

SEED_FILE = "/data/seed.txt"
ENCRYPTED_SEED = "/app/encrypted_seed.txt"
PRIVATE_KEY_FILE = "/app/student_private.pem"

def decrypt_seed_route():
    try:
        # Read encrypted seed
        with open(ENCRYPTED_SEED, "r") as f:
            encrypted_seed_b64 = f.read().strip()

        # Load private key
        with open(PRIVATE_KEY_FILE, "rb") as f:
            private_key = serialization.load_pem_private_key(f.read(), password=None)

        encrypted_seed = base64.b64decode(encrypted_seed_b64)

        # Decrypt
        decrypted_bytes = private_key.decrypt(
            encrypted_seed,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        hex_seed = decrypted_bytes.decode("utf-8")

        # Validate seed length
        if len(hex_seed) != 64:
            raise HTTPException(status_code=400, detail="Invalid seed length")

        # Save to /data/seed.txt (persistent volume)
        with open(SEED_FILE, "w") as f:
            f.write(hex_seed)

        return {"status": "success", "seed_saved": True}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
