import uuid

from sqlalchemy import String, UUID
from sqlalchemy.orm import mapped_column, Mapped, relationship

from core.base_model import Base
from notes.models import Note


class User(Base):
    __tablename__ = "users"  # noqa

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    login: Mapped[str] = mapped_column(String)
    password: Mapped[str] = mapped_column(String)
    notes: Mapped[Note] = relationship(backref="user", lazy="joined")
