from typing import Awaitable, Callable

from fastapi import Request, Response
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

from backend.database import interface
from backend.database.database import create_db_session


class HandleInit(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Response]],
    ) -> Response:
        game_interface = interface.GameInterface()
        print(request.url.path)
        if request.url.path == "/api/games" and not game_interface.get_games(
            next(create_db_session())
        ):
            return RedirectResponse(url="/api/init")
        return await call_next(request)
