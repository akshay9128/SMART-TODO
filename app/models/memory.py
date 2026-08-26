from datetime import datetime

from sqlalchemy import DateTime,ForeignKey,Integer,String,Text
from sqlalchemy.orm import Mapped,mapped_column
from app.database.base import Base

class UserMemory(Base):
    __tablename__="user_memories"

    id:Mapped[int]=mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id:Mapped[int]=mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    memory_type:Mapped[str]=mapped_column(
        String(50),
        nullable=False
    )

    key:Mapped[str]=mapped_column(
        String(100),
        nullable=False
    )

    value:Mapped[str]=mapped_column(
        Text,
        nullable=False
    )

    created_at:Mapped[datetime]=mapped_column(
        DateTime,
        default=datetime.now,
        nullable=False
    )

    updated_at:Mapped[datetime]=mapped_column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
        nullable=False
    )