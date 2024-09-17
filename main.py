from fastapi import FastAPI

from notes.endpoints import router


app = FastAPI(
    title="Notes App"
)

app.include_router(router, prefix="/note", tags=["Notes"])
