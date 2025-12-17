import time
from totp_utils import generate_totp_code

with open("/data/seed.txt") as f:
    seed = f.read().strip()

code = generate_totp_code(seed)
valid_for = 30 - (int(time.time()) % 30)

print(code)
print("valid_for:", valid_for)
