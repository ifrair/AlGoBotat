from uuid import UUID

from loguru import logger
from sqlalchemy import select, update, delete

from db.engineer import DbEngine
from db.model import DBCourseAssignment


class CourseAssignmentRepo:
    def __init__(self):
        self.db = DbEngine()

    def get_by_id(self, assignment_id: UUID) -> DBCourseAssignment | None:
        with self.db.get_session() as session:
            stmt = select(DBCourseAssignment).where(DBCourseAssignment.id == assignment_id)
            result = session.execute(stmt).unique().scalar_one_or_none()

        return result

    def get_by_user(self, user_id: UUID) -> list[DBCourseAssignment]:
        with self.db.get_session() as session:
            stmt = (
                select(DBCourseAssignment)
                .where(DBCourseAssignment.user_id == user_id)
                .order_by(DBCourseAssignment.status)
            )
            result = session.execute(stmt).unique().scalars().all()

        return list(result)

    def get_by_course_and_user(self, course_id: UUID, user_id: UUID) -> DBCourseAssignment | None:
        with self.db.get_session() as session:
            stmt = (
                select(DBCourseAssignment)
                .where(
                    DBCourseAssignment.course_id == course_id,
                    DBCourseAssignment.user_id == user_id,
                )
                .limit(1)
            )
            result = session.execute(stmt).unique().scalar_one_or_none()

        return result

    def list_all(self) -> list[DBCourseAssignment]:
        with self.db.get_session() as session:
            stmt = select(DBCourseAssignment).order_by(DBCourseAssignment.status)
            result = session.execute(stmt).unique().scalars().all()

        return list(result)

    def list_by_user(self, user_id: UUID) -> list[DBCourseAssignment]:
        with self.db.get_session() as session:
            stmt = (
                select(DBCourseAssignment)
                .where(DBCourseAssignment.user_id == user_id)
                .order_by(DBCourseAssignment.status)
            )
            result = session.execute(stmt).unique().scalars().all()

        return list(result)

    def create(self, course_id: UUID, user_id: UUID) -> DBCourseAssignment:
        with self.db.get_session() as session:
            assignment = DBCourseAssignment(
                course_id=course_id,
                user_id=user_id,
                status="uncompleted",
                progress_percentage=0.0,
                progress={},
            )
            session.add(assignment)
            session.flush()
            logger.info(
                "Course assignment created: course=%s user=%s id=%s",
                course_id, user_id, assignment.id,
            )

        return assignment

    def update_status(self, assignment_id: UUID, status: str) -> DBCourseAssignment | None:
        with self.db.get_session() as session:
            stmt = select(DBCourseAssignment).where(DBCourseAssignment.id == assignment_id)
            assignment = session.execute(stmt).unique().scalar_one_or_none()
            if not assignment:
                return None
            assignment.status = status
            session.flush()
            logger.info("Assignment %s status set to %s", assignment_id, status)

        return assignment

    def update_content_status(
        self, assignment_id: UUID, item_id: str, status: str
    ) -> DBCourseAssignment | None:
        with self.db.get_session() as session:
            stmt = select(DBCourseAssignment).where(DBCourseAssignment.id == assignment_id)
            assignment = session.execute(stmt).unique().scalar_one_or_none()
            if not assignment:
                return None
            progress = assignment.progress or {}
            content = progress.get("content", {})
            content[item_id] = status
            progress["content"] = content
            assignment.progress = progress
            session.flush()
            logger.info(
                "Assignment %s content item %s status set to %s",
                assignment_id, item_id, status,
            )

        return assignment

    def add_task_submission(
        self, assignment_id: UUID, item_id: str, submission_id: str
    ) -> DBCourseAssignment | None:
        with self.db.get_session() as session:
            stmt = select(DBCourseAssignment).where(DBCourseAssignment.id == assignment_id)
            assignment = session.execute(stmt).unique().scalar_one_or_none()
            if not assignment:
                return None
            progress = assignment.progress or {}
            submissions = progress.get("submissions", {})
            submissions[item_id] = submission_id
            progress["submissions"] = submissions
            assignment.progress = progress
            session.flush()
            logger.info(
                "Assignment %s task %s submission %s added",
                assignment_id, item_id, submission_id,
            )

        return assignment
