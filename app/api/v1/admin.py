from fastapi import APIRouter, Depends, status, Query
from sqlalchemy.orm import Session


from app.auth.permissions import require_admin
from app.database.session import get_db
from app.dependencies.roles import get_current_admin
from app.models.user import User
from app.schemas.admin import AdminUserCreate, UserResponse
from app.schemas.user import UserListResponse
from app.services.admin_service import AdminService
from app.services.user_services import UserService

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)


@router.post(
    "/users",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    user_data: AdminUserCreate,
    db: Session = Depends(get_db),
    current_admin: User = Depends(get_current_admin),
):
    return AdminService.create_user(
        db=db,
        user_data=user_data,
    )

@router.get(
    "/users",
    response_model=UserListResponse,
)
def list_users(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    return UserService.list_users(
        db=db,
        page=page,
        size=size,
    )