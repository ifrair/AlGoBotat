from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from api.dependencies import get_current_user_id, require_admin
from db.course_assignment_repo import CourseAssignmentRepo
from service.schemes import (
    CourseAssignmentCreate,
    CourseAssignmentResponse,
    StatusUpdate,
    ContentStatusUpdate,
    TaskSubmission,
)
from db.user_repo import UserRepo

router = APIRouter()
assignment_repo = CourseAssignmentRepo()
user_repo = UserRepo()


@router.post("/api/v1/admin/course_assignment")
def admin_create_assignment(data: CourseAssignmentCreate, _=Depends(require_admin)):
    if not data.user_id:
        raise HTTPException(status_code=400, detail="user_id is required for admin assignment")
    assignment = assignment_repo.create(course_id=data.course_id, user_id=data.user_id)
    return {"id": assignment.id}


@router.post("/api/v1/course_assignment")
def create_self_assignment(data: CourseAssignmentCreate, auth=Depends(get_current_user_id)):
    user_id, _ = auth
    assignment = assignment_repo.create(course_id=data.course_id, user_id=user_id)

    return {"id": assignment.id}


@router.get("/api/v1/course_assignment/{assignment_id}", response_model=CourseAssignmentResponse)
def get_assignment(assignment_id: UUID, auth=Depends(get_current_user_id)):
    user_id, _ = auth
    assignment = assignment_repo.get_by_id(assignment_id)
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    if assignment.user_id != user_id:
        raise HTTPException(status_code=403, detail="Access denied")
    return assignment


@router.get("/api/v1/course_assignment/admin/{assignment_id}", response_model=CourseAssignmentResponse)
def admin_get_assignment(assignment_id: UUID, _=Depends(require_admin)):
    assignment = assignment_repo.get_by_id(assignment_id)
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    return assignment


@router.get("/api/v1/course_assignments", response_model=list[CourseAssignmentResponse])
def list_user_assignments(auth=Depends(get_current_user_id)):
    user_id, _ = auth
    assignments = assignment_repo.list_by_user(user_id)
    return assignments


@router.get("/api/v1/admin/course_assignments", response_model=list[CourseAssignmentResponse])
def admin_list_all_assignments(_=Depends(require_admin)):
    assignments = assignment_repo.list_all()
    return assignments


@router.get(
    "/api/v1/admin/course_assignments/{target_user_id}",
    response_model=list[CourseAssignmentResponse],
)
def admin_list_user_assignments(target_user_id: UUID, _=Depends(require_admin)):
    assignments = assignment_repo.list_by_user(target_user_id)
    return assignments


@router.post("/internal/v1/course_assignments/{assignment_id}/content/{item_id}/status")
def internal_update_content_status(
    assignment_id: UUID,
    item_id: str,
    data: list[ContentStatusUpdate],
):
    if not data:
        raise HTTPException(status_code=400, detail="Empty status list")
    status = data[0].status
    assignment = assignment_repo.update_content_status(assignment_id, item_id, status)
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    return assignment.progress


@router.post("/internal/v1/course_assignments/{assignment_id}/task/{item_id}")
def internal_add_task_submission(
    assignment_id: UUID,
    item_id: str,
    data: TaskSubmission,
):
    assignment = assignment_repo.add_task_submission(assignment_id, item_id, data.item_id)
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    return assignment.progress


@router.post("/internal/v1/course_assignments/{assignment_id}/status")
def internal_update_assignment_status(
    assignment_id: UUID,
    data: StatusUpdate,
):
    assignment = assignment_repo.update_status(assignment_id, data.status)
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")
    return {"status": assignment.status}
