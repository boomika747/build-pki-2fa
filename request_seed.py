import base64
import json
import requests

STUDENT_ID = "YOUR_STUDENT_ID"  # replace with your student ID
GITHUB_REPO = "https://github.com/SreenitaPadarthi06/pki-2fa.git"

with open("student_public.pem", "r") as f:
    public_key = f.read()

payload = {
    "student_id": STUDENT_ID,
    "github_repo_url": GITHUB_REPO,
    "public_key": public_key
}

response = requests.post(
    "https://eajeyq4r3zljoq4rpovy2nthda0vtjqf.lambda-url.ap-south-1.on.aws",
    json=payload
)

data = response.json()
if data.get("status") == "success":
    encrypted_seed = data["encrypted_seed"]
    with open("encrypted_seed.txt", "w") as f:
        f.write(encrypted_seed)
    print("Encrypted seed saved to encrypted_seed.txt")
else:
    print("Error requesting seed:", data)
