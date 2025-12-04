import time
from totp_utils import generate_totp_code


# Read hex seed from file created earlier
with open("data/seed.txt", "r") as f:

    hex_seed = f.read().strip()

code = generate_totp_code(hex_seed)

valid_for = 30 - (int(time.time()) % 30)  # seconds remaining in current period

print(code)
print("valid_for:", valid_for)
