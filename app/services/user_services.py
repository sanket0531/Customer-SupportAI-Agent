import math

from sqlalchemy.orm import Session

from app.repositories.user_repository import UserRepository


class UserService:

    @staticmethod
    def list_users(
        db: Session,
        page: int,
        size: int,
    ) -> dict:

        offset = (page - 1) * size

        users = UserRepository.get_users(
            db=db,
            offset=offset,
            limit=size,
        )

        total = UserRepository.count_users(db=db)

        return {
            "items": users,
            "page": page,
            "size": size,
            "total": total,
            "pages": math.ceil(total / size),
        }