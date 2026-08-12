from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr
from db.model import DBUser


class UserResponse(BaseModel):
    id: UUID
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    bio: str | None = None
    email: str | None = None
    photo_url: str | None = None
    role: str = "USER"
    is_banned: bool = False
    is_test_user: bool = False
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}

class UserResponseProvider:
    @staticmethod
    def from_user_db(user: DBUser):
        return UserResponse(id=user.id, username=user.username, first_name=user.first_name, last_name=user.last_name, bio=user.bio, email=user.email, photo_url=user.photo_url, role=user.role, is_banned=user.is_banned, is_test_user=user.is_test_user, created_at=user.created_at, updated_at=user.updated_at )


class UserYandex(BaseModel):
    id: int
    login: str
    default_email: EmailStr
    emails: list[EmailStr] = []

    real_name: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    display_name: str | None = None
    birthday: str | None = None
    default_phone: dict | None = None
    default_avatar_id: str | None = None

    def __hash__(self):
        return hash(
            (type(self),) + tuple(getattr(self, f) for f in self.model_fields.keys())
        )

    def __eq__(self, other):
        return hash(self) == hash(other)


class CourseAssignmentCreate(BaseModel):
    course_id: UUID
    user_id: UUID | None = None


class CourseAssignmentResponse(BaseModel):
    id: UUID
    course_id: UUID
    user_id: UUID
    status: str = "uncompleted"
    progress_percentage: float = 0
    progress: dict = {}

    model_config = {"from_attributes": True}


class CourseAssignmentProgressContent(BaseModel):
    content: dict[str, str] = {}
    submissions: dict[str, str] = {}


class CourseAssignmentAdminTask(BaseModel):
    last_submission_id: str | None = None
    submissions: list[str] = []


class CourseAssignmentAdminProgress(BaseModel):
    content: dict[str, str] = {}
    task: CourseAssignmentAdminTask | None = None


class CourseAssignmentAdminResponse(BaseModel):
    id: UUID
    course_id: UUID
    user_id: UUID
    status: str = "uncompleted"
    progress_percentage: float = 0
    progress: dict = {}

    model_config = {"from_attributes": True}


class StatusUpdate(BaseModel):
    status: str


class ContentStatusUpdate(BaseModel):
    status: str


class TaskSubmission(BaseModel):
    item_id: str
