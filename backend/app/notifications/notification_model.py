import enum
from datetime import UTC, datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import TYPE_CHECKING

from app.db.database import Base


if TYPE_CHECKING:
    from app.users.user_model import UserModel


class NotificationChannel(str, enum.Enum):
    EMAIL = "email"
    SMS = "sms"
    PUSH = "push"


class NotificationStatus(str, enum.Enum):
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"


class NotificationModel(Base):
    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    title: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    recipient: Mapped[str] = mapped_column(String(255), nullable=False)

    channel: Mapped[NotificationChannel] = mapped_column(
        Enum(
            NotificationChannel,
            values_callable=lambda enum_class: [member.value for member in enum_class],
        ),
        nullable=False
    )

    status: Mapped[NotificationStatus] = mapped_column(
        Enum(
            NotificationStatus,
            values_callable=lambda enum_class: [member.value for member in enum_class],
        ),
        nullable=False
    )

    creation_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
    )

    user: Mapped["UserModel"] = relationship(
        "UserModel",
        back_populates="notifications"
    )