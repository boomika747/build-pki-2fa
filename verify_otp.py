from totp_utils import verify_totp_code

with open("/data/seed.txt") as f:
    seed = f.read().strip()

code = input("Enter 6-digit code: ").strip()
print("valid:", verify_totp_code(seed, code))
