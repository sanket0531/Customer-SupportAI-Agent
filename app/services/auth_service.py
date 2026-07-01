from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate
from app.utils.hashing import hash_password


class AuthService:

    @staticmethod
    def register_user(
        db: Session,
        user_data: UserCreate
    ):

        existing = UserRepository.get_by_email(
            db,
            user_data.email
        )

        if existing:
            raise HTTPException(
                status_code=400,
                detail="Email already exists."
            )

        user = User(
            full_name=user_data.full_name,
            email=user_data.email,
            password=hash_password(
                user_data.password
            )
        )

        return UserRepository.create_user(
            db,
            user
        )