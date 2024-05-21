from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from ..database import database, interface
from ..schemas.game import GameSchema
from ..service import handle_wiki

router = APIRouter(prefix="/api", tags=["api"])

game_interface = interface.GameInterface()


@router.get(path="/test", tags=["test"])
async def get_test() -> dict[str, str | int]:
    return {"message": "OKAY", "status": status.HTTP_200_OK}


@router.get(path="/games", tags=["games"], response_model=list[GameSchema])
async def get_games(
    db: Session = Depends(database.create_db_session),
) -> list[GameSchema] | None:
    games = await handle_wiki.get_all_games()
    result = game_interface.insert_games(games, db)
    if result:
        return [GameSchema.model_validate(game) for game in result]
    return None
