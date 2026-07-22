from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from service.schemes import UserYandex
from service.user_servcie import UserService
from api.dependencies import get_current_user_id, require_admin
from db.user_repo import UserRepo
from service.schemes import UserResponse

router = APIRouter()
user_service = UserService()

@router.get("/api/v1/admin/user/{user_id}", response_model=UserResponse)
def admin_get_user(user_id: UUID, _=Depends(require_admin)):
    return user_service.get_user_profile(user_id=user_id)

@router.post("/api/v1/user", response_model=UserResponse)
def get_or_create_user(data: UserYandex, _=Depends(require_admin)):
     return user_service.save_user_or_get_profile_from_yandex(yandex_sso=data)

@router.get("/api/v1/admin/find_by_email/{email}", response_model=UserResponse)
def admin_find_by_yandex_id(email: str, _=Depends(require_admin)):
    return user_service.get_user_profile_by_email(email= email)
