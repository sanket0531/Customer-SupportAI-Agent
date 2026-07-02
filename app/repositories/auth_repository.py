from sqlalchemy.orm import Session

from app.models.user import User


class AuthRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_email(self, email: str):
        """
        Fetch a user by email.
        Returns a User object if found, otherwise None.
        """
        return (
            self.db.query(User)
            .filter(User.email == email)
            .first()
        )