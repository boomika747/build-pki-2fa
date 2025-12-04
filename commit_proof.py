import base64, subprocess
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

# get latest commit hash
commit_hash = subprocess.check_output(["git", "rev-parse", "HEAD"]).decode().strip()

# load student private key
with open("student_private.pem","rb") as f:
    priv = serialization.load_pem_private_key(f.read(), password=None)

# sign commit hash (ASCII)
signature = priv.sign(
    commit_hash.encode("utf-8"),
    padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
    hashes.SHA256()
)

# load instructor public key
with open("instructor_public.pem","rb") as f:
    instr_pub = serialization.load_pem_public_key(f.read())

# encrypt signature using instructor public key (OAEP SHA-256)
enc = instr_pub.encrypt(
    signature,
    padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
)

print("Commit Hash:", commit_hash)
print("Encrypted Signature (base64):")
print(base64.b64encode(enc).decode())
