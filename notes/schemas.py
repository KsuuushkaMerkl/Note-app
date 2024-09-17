from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class NoteSchema(BaseModel):
    """
    Note schema.
    """
    id: UUID
    title: str
    content: str
    tags: list[str]
    created_at: datetime
    updated_at: datetime


class CreateNoteRequestSchema(BaseModel):
    """
    Create note request schema.
    """
    title: str
    content: str
    tags: list[str]


class CreateNoteResponseSchema(BaseModel):
    """
    Create note response schema.
    """
    id: UUID
    title: str
    content: str
    tags: list[str]
    created_at: datetime


class UpdateNoteRequestSchema(BaseModel):
    """
    Update note request schema.
    """
    title: str | None = None
    content: str | None = None
    tags: list[str] | None = None


class UpdateNoteResponseSchema(BaseModel):
    """
    Update note response schema.
    """
    id: UUID
    title: str
    content: str
    tags: list[str]
    updated_at: datetime
    

class NotesTagSchema(BaseModel):
    tags: list[str]
