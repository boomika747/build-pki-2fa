import base64
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes

with open("encrypted_seed.txt", "r") as f:
    encrypted_seed_b64 = f.read()

with open("student_private.pem", "rb") as f:
    private_key = serialization.load_pem_private_key(f.read(), password=None)

encrypted_seed = base64.b64decode(encrypted_seed_b64)

decrypted_bytes = private_key.decrypt(
    encrypted_seed,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

hex_seed = decrypted_bytes.decode("utf-8")
if len(hex_seed) != 64:
    raise ValueError("Seed is not 64-character hex")
with open("data/seed.txt", "w") as f:
    f.write(hex_seed)
print("Seed decrypted and saved to data/seed.txt")
