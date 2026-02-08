from passlib.context import CryptContext
from fastapi import HTTPException, status
from datetime import timedelta, datetime, timezone
import jwt
from src.config import Config
import uuid
passwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)

ACCESS_TOKEN_EXPIRE = 3600

def generate_password_hash(password: str) -> str:
    hashed_password = passwd_context.hash(password)
    return hashed_password

def verify_password(password: str, hashed_password: str) -> bool:
    return passwd_context.verify(password, hashed_password)

def create_access_token(
    user_data: dict,
    expiry: timedelta | None = None,
    refresh: bool = False
):
    payload = user_data.copy()

    now = datetime.now(timezone.utc)

    payload["user"] = user_data
    payload["iat"] = now
    payload["exp"] = now + (expiry if expiry else timedelta(seconds=ACCESS_TOKEN_EXPIRE))
    payload["jti"] = str(uuid.uuid4())
    payload["refresh"] = refresh

    token = jwt.encode(
        payload=payload,
        key=Config.JWT_SECRET,
        algorithm=Config.JWT_ALGORITHM
    )

    return token

def decode_token(token: str) -> dict:
    try:
        token_data = jwt.decode(
            jwt=token,
            key=Config.JWT_SECRET,
            algorithms=[Config.JWT_ALGORITHM]
        )
        print(f"Decoded token data: {token_data}")
        return token_data
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )