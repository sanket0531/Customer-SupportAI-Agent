from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.utils.hashing import hash_password
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.admin import AdminUserCreate


class AdminService:

    @staticmethod
    def create_user(
        db: Session,
        user_data: AdminUserCreate,
    ) -> User:

        existing_user = UserRepository.get_by_email(
            db,
            user_data.email,
        )

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered.",
            )

        user = User(
            full_name=user_data.full_name,
            email=user_data.email,
            password=hash_password(user_data.password),
            role=user_data.role,
        )

        return UserRepository.create_user(
            db,
            user,
        )