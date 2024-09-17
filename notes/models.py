import uuid
from datetime import datetime

from sqlalchemy import String, UUID, DateTime, ARRAY, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from core.base_model import Base


class Note(Base):
    __tablename__ = "notes"  # noqa

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    title: Mapped[str] = mapped_column(String)
    content: Mapped[str] = mapped_column(String)
    tags: Mapped[list[str]] = mapped_column(type_=ARRAY(String), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(), nullable=False)
