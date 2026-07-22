"""Add course_assignment table and photo_url column

Revision ID: bb8f6e2a1c3d
Revises: bf42e0d31d92
Create Date: 2026-07-05 13:48:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "bb8f6e2a1c3d"
down_revision: Union[str, Sequence[str], None] = "bf42e0d31d92"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "user_yandex_sso",
        "user_id",
        existing_type=sa.UUID(),
        existing_nullable=True,
        new_column_type=sa.UUID(),
    )
    op.drop_constraint(
        "user_yandex_sso_user_id_fkey",
        "user_yandex_sso",
        type_="foreignkey",
    )
    op.create_foreign_key(
        "user_yandex_sso_user_id_fkey",
        "user_yandex_sso",
        "user",
        ["user_id"],
        ["id"],
        ondelete="CASCADE",
    )
    op.alter_column(
        "user",
        "photo_url",
        existing_type=sa.String(length=64),
        type_=sa.String(length=256),
        existing_nullable=True,
    )
    op.create_table(
        "course_assignment",
        sa.Column("id", sa.UUID(), server_default=sa.text("gen_random_uuid()"), nullable=False),
        sa.Column("course_id", sa.UUID(), nullable=False),
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("status", sa.String(length=32), server_default="uncompleted", nullable=True),
        sa.Column("progress_percentage", sa.Float(), server_default="0", nullable=True),
        sa.Column("progress", postgresql.JSON(), server_default="{}", nullable=True),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("course_assignment")
    op.alter_column(
        "user",
        "photo_url",
        existing_type=sa.String(length=256),
        type_=sa.String(length=64),
        existing_nullable=True,
    )
    op.drop_constraint(
        "user_yandex_sso_user_id_fkey",
        "user_yandex_sso",
        type_="foreignkey",
    )
    op.create_foreign_key(
        "user_yandex_sso_user_id_fkey",
        "user_yandex_sso",
        "users",
        ["user_id"],
        ["id"],
        ondelete="CASCADE",
    )
