from chromadb import db
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.auth.jwt_handler import create_access_token
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate
from app.utils.hashing import hash_password, verify_password

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
    
    
    @staticmethod
    def login_user(
        db: Session,
        email: str,
        password: str
    ):
        user = UserRepository.get_by_email(
            db,
            email
        )

        if not user:
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password"
            )

        if not verify_password(
            password,
            user.password
        ):
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password"
            )

        access_token = create_access_token(
            {
                "sub": str(user.id),
                "email": user.email
            }
        )

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }