from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from fastapi import FastAPI

from .api import api, middleware
from .database.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[Any, Any]:
    init_db()
    yield


app = FastAPI(debug=True, lifespan=lifespan)

app.include_router(api.router)
app.add_middleware(middleware.HandleInit)
