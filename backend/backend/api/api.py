from typing import Any

from fastapi import APIRouter, status

from ..service import handle_wiki

router = APIRouter(prefix="/api", tags=["api"])


@router.get(path="/test", tags=["test"])
async def get_test() -> dict[str, str | int]:
    return {"message": "OKAY", "status": status.HTTP_200_OK}


@router.get(path="/games", tags=["games"])
async def get_games() -> dict[str, Any]:
    try:
        games = await handle_wiki.get_all_games()
        return {
            "message": "Okay",
            "games": games,
            "amount_of_games": len(games),
            "status": status.HTTP_200_OK,
        }
    except Exception as e:
        return {"message": e}
