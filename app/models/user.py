from datetime import datetime

from sqlalchemy import DateTime,String
from sqlalchemy.orm import Mapped,mapped_column

from app.database.base import Base

class User(Base):
    __tablename__="users"

    id:Mapped[int]=mapped_column(
        primary_key=True,
        index=True
    )

    username:Mapped[str]=mapped_column(
        String(100),
        unique=True,
        nullable=False,
        index=True
    )

    email:Mapped[str]=mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )

    hashed_password:Mapped[str]=mapped_column(
        String(255),
        nullable=False
    )

    created_at:Mapped[datetime]=mapped_column(
        DateTime,
        default=datetime.now,
        nullable=False
    )