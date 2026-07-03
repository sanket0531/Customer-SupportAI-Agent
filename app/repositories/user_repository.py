from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:

    @staticmethod
    def get_by_email(
        db: Session,
        email: str,
    ) -> User | None:
        stmt = select(User).where(User.email == email)
        return db.scalar(stmt)

    @staticmethod
    def get_by_id(
        db: Session,
        user_id: int,
    ) -> User | None:
        stmt = select(User).where(User.id == user_id)
        return db.scalar(stmt)

    @staticmethod
    def create_user(
        db: Session,
        user: User,
    ) -> User:
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def get_users(
        db: Session,
        limit: int,
        offset: int,
    ) -> list[User]:
        stmt = (
            select(User)
            .offset(offset)
            .limit(limit)
        )

        return list(db.scalars(stmt).all())
    
    @staticmethod
    def count_users(db: Session) -> int:
        statement = select(func.count()).select_from(User)

        return db.execute(statement).scalar_one()