from datetime import datetime
from uuid import UUID

from core.schemas import Schemas


class NoteSchema(Schemas):
    """
    Note schema.
    """
    id: UUID
    title: str
    content: str
    tags: list[str]
    created_at: datetime
    updated_at: datetime


class CreateNoteRequestSchema(Schemas):
    """
    Create note request schema.
    """
    title: str
    content: str
    tags: list[str]


class CreateNoteResponseSchema(Schemas):
    """
    Create note response schema.
    """
    id: UUID
    title: str
    content: str
    tags: list[str]
    created_at: datetime


class UpdateNoteRequestSchema(Schemas):
    """
    Update note request schema.
    """
    title: str | None = None
    content: str | None = None
    tags: list[str] | None = None


class UpdateNoteResponseSchema(Schemas):
    """
    Update note response schema.
    """
    id: UUID
    title: str
    content: str
    tags: list[str]
    updated_at: datetime
    

class NotesTagSchema(Schemas):
    tags: list[str]
