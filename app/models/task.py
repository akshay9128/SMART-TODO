from datetime import datetime
from sqlalchemy import String, Integer,DateTime,ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id:Mapped[int]=mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    title: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    completed: Mapped[bool]= mapped_column(
        default=False,
        nullable=False
    )

    category:Mapped[str]=mapped_column(
        String,
        default="General",
        nullable=False
    )

    priority:Mapped[str]=mapped_column(
        String,
        default="medium",
        nullable=False
    )

    due_at:Mapped[datetime | None]=mapped_column(
        DateTime,
        nullable=True
    )
    reminded:Mapped[bool]=mapped_column(
        default=False,
        nullable=False
    )