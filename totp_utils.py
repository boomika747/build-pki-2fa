import pyotp
import base64

def generate_totp_code(hex_seed: str) -> str:
    seed_bytes = bytes.fromhex(hex_seed)
    base32_seed = base64.b32encode(seed_bytes).decode()
    return pyotp.TOTP(base32_seed).now()

def verify_totp_code(hex_seed: str, code: str) -> bool:
    seed_bytes = bytes.fromhex(hex_seed)
    base32_seed = base64.b32encode(seed_bytes).decode()
    return pyotp.TOTP(base32_seed).verify(code)
