from sqlalchemy import Integer, String, text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from app.db.database import Base
from app.notifications import notification_model  # noqa: F401

if TYPE_CHECKING:
    from app.notifications.notification_model import NotificationModel

class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(200), nullable=False)
    pokemon_team: Mapped[list[int]] = mapped_column(
        ARRAY(Integer),
        default=list,
        server_default=text("'{}'::integer[]"),
        nullable=False
    )

    notifications: Mapped[list["NotificationModel"]] = relationship(
        "NotificationModel",
        back_populates="user",
        cascade="all, delete-orphan"
    )