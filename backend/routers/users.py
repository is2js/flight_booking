from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, HTTPException, status, Depends, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from backend.crud.database import get_session
from backend.crud.users import get_user_by_email, create_user
from backend.external_services.email import send_email_async
from backend.schemas.auth import Token
from backend.schemas.users import UserRead, UserCreate
from backend.utils.security import (
    authenticate_user,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
)

router = APIRouter()


@router.post("/register/", response_model=UserRead)
async def register(
    user_in: UserCreate,
    background_tasks: BackgroundTasks,
    session: Session = Depends(get_session),
):
    # unique칼럼으로 존재여부 확인
    user = get_user_by_email(session, user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    # DB에 유저 생성
    user = create_user(session, user_in.email, user_in.password)

    # send email
    subject = "회원가입을 축하드려요."
    recipients = [user_in.email]
    body_text = f"안녕하세요, {user.email}님! 회원가입을 축하드립니다."
    # await send_email_async(subject, recipients, body_text)
    background_tasks.add_task(send_email_async, subject, recipients, body_text)

    return user


@router.post("/token/")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Session = Depends(get_session),
) -> Token:
    # email존재여부 -> 패스워드 여부 -> 통과시 UserInDB객체 or False
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # 만료기간정보 생성
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.email)},  # email을 sub로
        expires_delta=access_token_expires,
    )

    return Token(access_token=access_token, token_type="bearer")
