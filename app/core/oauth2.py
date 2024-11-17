from typing import Annotated
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.database import settings, database
from app.user import user_schema, user_model
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import Optional

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minute


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_key")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(key=user_id)
    except JWTError:
        raise credentials_exception
    return token_data


def get_current_user(db: database, token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = verify_token(token, credentials_exception)
    data = (
        db.query(user_schema.UserTable)
        .filter(user_schema.UserTable.key == token_data.key)
        .first()
    )
    if data is None:
        raise credentials_exception
    return data


# current_user dependency injection
authUser = Annotated[user_schema.UserTable, Depends(get_current_user)]


# token data model
class TokenData(BaseModel):
    key: Optional[str] = None
