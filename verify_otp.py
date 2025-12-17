from pydantic import BaseModel

class VerifyRequest(BaseModel):
    code: str

@app.post("/verify-2fa")
def verify_2fa(req: VerifyRequest):
    try:
        with open("/data/last_code.txt", "r") as f:
            last_code = f.read().strip()
    except FileNotFoundError:
        return {"valid": False}

    return {"valid": req.code == last_code}
