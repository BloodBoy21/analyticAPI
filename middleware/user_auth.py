import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
import os
from services.analytic_services import get_service_by_id
from models.process import AnalyticProcess

JWT_SECRET = os.getenv("JWT_SECRET")


async def auth_user(auth: str = Depends(HTTPBearer())) -> AnalyticProcess:
    try:
        payload = jwt.decode(auth.credentials, JWT_SECRET, algorithms=["HS256"])
        return get_service_by_id(payload["process_id"])
    except jwt.exceptions.InvalidSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    except jwt.exceptions.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Expired token",
        )
    except jwt.exceptions.DecodeError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
