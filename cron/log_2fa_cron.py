#!/usr/local/bin/python3

import sys
import os
import datetime

# IMPORTANT: allow cron to find project modules
sys.path.append("/app")

from totp_utils import generate_totp_code

SEED_FILE = "/data/seed.txt"
OUT_FILE = "/data/last_code.txt"

if os.path.exists(SEED_FILE):
    with open(SEED_FILE, "r") as f:
        seed = f.read().strip()

    code = generate_totp_code(seed)
    ts = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    with open(OUT_FILE, "a") as f:
        f.write(f"{ts} 2FA Code: {code}\n")
