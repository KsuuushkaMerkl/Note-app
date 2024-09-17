from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import scoped_session
from fastapi.encoders import jsonable_encoder

from core.database import get_session
from notes.models import Note
from notes.schemas import NoteSchema, CreateNoteRequestSchema, CreateNoteResponseSchema, \
    UpdateNoteRequestSchema, UpdateNoteResponseSchema, NotesTagSchema

router = APIRouter()


@router.post('/', response_model=CreateNoteResponseSchema)
async def create_note(
        data: CreateNoteRequestSchema,
        db: scoped_session = Depends(get_session)
):
    """
    Create new note.
    """
    note = Note(**data.model_dump())
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


@router.get('/', response_model=list[NoteSchema])
async def get_notes(
        db: scoped_session = Depends(get_session)
):
    """
    Get all notes.
    """
    return db.query(Note).all()


@router.post('/search_by_tags', response_model=list[NoteSchema])
async def get_note_by_tags(
        data: NotesTagSchema,
        db: scoped_session = Depends(get_session)
):
    """
    Get note by tags.
    """
    return db.query(Note).filter(Note.tags.any(*data.tags)).all()


@router.get('/{note_id}', response_model=NoteSchema)
async def get_note_by_id(
        note_id: UUID,
        db: scoped_session = Depends(get_session)
):
    """
    Get note by id.
    """
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        return HTTPException(
            status_code=404,
            detail="Note not found."
        )
    return note


@router.patch('/{note_id}', response_model=UpdateNoteResponseSchema)
async def update_note(
        note_id: UUID,
        data: UpdateNoteRequestSchema,
        db: scoped_session = Depends(get_session)
):
    """
    Update note by id.
    """
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        return HTTPException(
            status_code=404,
            detail="Note not found."
        )
    obj_data = jsonable_encoder(note)  # noqa
    update_data = data.model_dump(exclude_unset=True)
    for field in obj_data:
        if field in update_data:
            setattr(note, field, update_data[field])
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


@router.delete('/{note_id}')
async def delete_note(
        note_id: UUID,
        db: scoped_session = Depends(get_session)
):
    """
    Delete note.
    """
    note = db.query(Note).filter(Note.id == note_id).delete()
    if note == 0:
        return HTTPException(
            status_code=404,
            detail="Note not found."
        )
    return {"id": note_id}

