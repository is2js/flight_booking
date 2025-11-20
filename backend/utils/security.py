import os
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from passlib.context import CryptContext
from sqlmodel import Session, select

from backend.crud.database import get_session
from backend.models.users import UserInDB

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(session: Session, email: str, password: str):
    user = session.exec(select(UserInDB).where(UserInDB.email == email)).first()
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # username/password docs입력 -> oauth2_scheme 의존성이 token endpoint 에서 유저정보 encode 를 통해 token 발급한 것을 가져옴
        # -> here token에서 유저정보 다시 decode해서 [user 유니크키인 email] 추출
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # 1) 토큰 속 email 존재유무 확인
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        # 2) email 로 유저 존재유무 확인
        # -> crud/users.py는 utils을 끌어다 쓰는 주체. 순환에러 남
        # -> 피동인 session으로 직접 조회
        # ImportError: cannot import name 'get_user_by_email' from partially initialized module 'backend.crud.users' (most likely due to a circular import)
        # user = get_user_by_email(session, email)
        user = session.exec(select(UserInDB).where(UserInDB.email == email)).first()
        if user is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception

    return user
