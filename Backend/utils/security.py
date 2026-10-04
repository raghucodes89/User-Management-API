from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv
import os


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(password: str, hashed_password: str):
    return pwd_context.verify(password, hashed_password)  

#   ==========================
# |     "JWT FUNCTION CODE"    |
#   ==========================

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"


def create_access_token(data : dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp" : expire})

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials
):
    token = credentials.credentials

    print("TOKEN RECEIVED:", token)

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except Exception as e:
        print("JWT ERROR:", e)
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )

def require_admin(current_user):
    if current_user.get("role") != "admin":
        raise HTTPException(
            status_code=403,
            detail="Admin access required"
        )
    return current_user

def require_manager(current_user):
    if current_user.get("role") not in ["admin", "manager"]:
        raise HTTPException(
            status_code=403,
            detail="Manager access required"
        )
    return current_user