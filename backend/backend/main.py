from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import api, custom_middleware
from .database.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[Any, Any]:
    init_db()
    yield


app = FastAPI(debug=True, lifespan=lifespan)

app.include_router(api.router)
app.add_middleware(
    custom_middleware.HandleInit,
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
