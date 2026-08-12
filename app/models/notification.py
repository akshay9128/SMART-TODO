from datetime import datetime

from sqlalchemy import Boolean,DateTime,ForeignKey,Integer,String
from sqlalchemy.orm import Mapped,mapped_column

from app.database.base import Base
from app.models.task import Task

class Notification(Base):
    __tablename__="notification"

    id: Mapped[int] = mapped_column(
            Integer,
            primary_key=True,
            index=True
        )

    user_id:Mapped[int]=mapped_column(
        ForeignKey("users.id"),
        nullable=True
    )

    task_id:Mapped[int]=mapped_column(
        ForeignKey("tasks.id"),
        nullable=False
    )

    message:Mapped[str]=mapped_column(
        String(500),
        nullable=False
    )

    is_read:Mapped[bool]=mapped_column(
        Boolean,default=False,
        nullable=False
    )

    created_at:Mapped[datetime]=mapped_column(
        DateTime,
        default=datetime.now,
        nullable=False
    )