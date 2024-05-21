from fastapi import FastAPI

from .api import api
from .database.database import init_db

app = FastAPI(debug=True)

app.include_router(api.router)


@app.on_event("startup")
async def startup() -> None:
    init_db()
