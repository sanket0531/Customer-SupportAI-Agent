from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.auth_schemas import LoginRequest
from app.schemas.user import UserCreate, UserResponse
from app.services.auth_service import AuthService

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"]
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    return AuthService.register_user(db, user)

@router.post("/login")
def login_json(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    return AuthService.login_user(
        db=db,
        email=login_data.email,
        password=login_data.password
    )


from fastapi.security import OAuth2PasswordRequestForm

@router.post("/token")
def login_oauth(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    return AuthService.login_user(
        db=db,
        email=form_data.username,
        password=form_data.password
    )