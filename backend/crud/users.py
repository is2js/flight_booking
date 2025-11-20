from typing import Optional

from pydantic import EmailStr
from sqlmodel import Session, select
from backend.models.users import UserInDB
from backend.utils.security import hash_password


def get_user_by_email(session: Session, email: EmailStr) -> Optional[UserInDB]:
    return session.exec(select(UserInDB).where(UserInDB.email == email)).first()


def create_user(session: Session, email: EmailStr, password: str) -> UserInDB:
    hashed_password = hash_password(password)
    user = UserInDB(
        email=email,
        # hashed_password=hashed_password,  # In real applications, hash the password!
        password=hashed_password,  # In real applications, hash the password!
    )
    session.add(user)  # Add the user to the session
    session.commit()  # Commit the transaction (push to DB)
    session.refresh(
        user
    )  # To get the generated ID and other defaults (return the user object with updated info)
    return user
