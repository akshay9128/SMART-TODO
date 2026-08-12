"""add user to notification

Revision ID: 665d400f7002
Revises: 2420f3e6f958
Create Date: 2026-08-12 17:50:48.584781

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '665d400f7002'
down_revision: Union[str, Sequence[str], None] = '2420f3e6f958'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # Add user_id to existing notifications
    with op.batch_alter_table("notification", schema=None) as batch_op:
        batch_op.add_column(
            sa.Column("user_id", sa.Integer(), nullable=True)
        )

        batch_op.create_foreign_key(
            "fk_notification_user_id_users",
            "users",
            ["user_id"],
            ["id"]
        )

    # Connect existing notifications to the owner of their task
    op.execute("""
        UPDATE notification
        SET user_id = (
            SELECT tasks.user_id
            FROM tasks
            WHERE tasks.id = notification.task_id
        )
        WHERE user_id IS NULL
    """)


def downgrade() -> None:
    """Downgrade schema."""

    with op.batch_alter_table("notification", schema=None) as batch_op:
        batch_op.drop_constraint(
            "fk_notification_user_id_users",
            type_="foreignkey"
        )

        batch_op.drop_column("user_id")