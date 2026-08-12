"""add user to tasks

Revision ID: 2420f3e6f958
Revises: f464bd40f080
Create Date: 2026-08-12 17:15:06.032611

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2420f3e6f958'
down_revision: Union[str, Sequence[str], None] = 'f464bd40f080'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    with op.batch_alter_table("tasks", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("user_id", sa.Integer(), nullable=True)
        )

        batch_op.create_foreign_key(
            "fk_tasks_user_id_users",
            "users",
            ["user_id"],
            ["id"]
        )

    # Assign existing tasks to testuser (id=1)
    op.execute(
        "UPDATE tasks SET user_id = 1 WHERE user_id IS NULL"
    )

def downgrade() -> None:
    """Downgrade schema."""

    with op.batch_alter_table("tasks", schema=None) as batch_op:
        batch_op.drop_constraint(
            "fk_tasks_user_id_users",
            type_="foreignkey"
        )

        batch_op.drop_column("user_id")
