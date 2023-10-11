import bcrypt
import jwt
import os
from datetime import datetime, timedelta

JWT_SECRET = os.getenv("JWT_SECRET")


def generate_token(process_id: int) -> str:
    payload = {
        "process_id": process_id,
        "exp": datetime.utcnow() + timedelta(days=30),
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
    return token
