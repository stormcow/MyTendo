from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from ..database import database, interface
from ..schemas.game import GameSchema
from ..service import generate_csv, handle_wiki

router = APIRouter(prefix="/api", tags=["api"])

game_interface = interface.GameInterface()


@router.get(path="/test", tags=["test"])
async def get_test() -> dict[str, str | int]:
    return {"message": "OKAY", "status": status.HTTP_200_OK}


@router.get(path="/init", tags=["init"], response_model=list[GameSchema])
async def init_games(
    db: Session = Depends(database.create_db_session),
) -> list[GameSchema] | HTTPException:
    games = await handle_wiki.get_all_games()
    result = game_interface.insert_games(games, db)
    if result:
        return [
            GameSchema.model_validate(game, from_attributes=True) for game in result
        ]
    return HTTPException(400)


@router.get(path="/games", tags=["games"], response_model=list[GameSchema])
async def get_games(
    db: Session = Depends(database.create_db_session),
) -> list[GameSchema] | HTTPException:
    result = game_interface.get_games(db)
    if result:
        return [
            GameSchema.model_validate(game, from_attributes=True) for game in result
        ]
    return HTTPException(400)


@router.put(path="/games", tags=["games"], response_model=list[GameSchema])
async def update_games(
    games: list[GameSchema], db: Session = Depends(database.create_db_session)
) -> list[GameSchema] | HTTPException:
    result = game_interface.update_games(db, games)
    return (
        [GameSchema.model_validate(game) for game in result]
        if result
        else HTTPException(400)
    )


@router.put(path="/game", tags=["game"], response_model=GameSchema)
async def update_game(
    game: GameSchema, db: Session = Depends(database.create_db_session)
) -> GameSchema | HTTPException:
    result = game_interface.update_game(db, game)
    return GameSchema.model_validate(result) if result else HTTPException(400)


@router.get(path="/game/{id}", tags=["game"], response_model=GameSchema)
async def get_game(
    id: int, db: Session = Depends(database.create_db_session)
) -> GameSchema | HTTPException:
    result = game_interface.get_game(db, id)
    return result if result else HTTPException(400)


@router.get(path="/csv", tags=["csv"], response_model=None)
async def get_csv(
    db: Session = Depends(database.create_db_session),
) -> StreamingResponse | HTTPException:
    games = game_interface.get_games(db)

    if not games:
        return HTTPException(400)

    return StreamingResponse(
        generate_csv.gen_csv([GameSchema.model_validate(game) for game in games]),
        media_type="test/csv",
        headers={"Content-Disposition": "attachment; filename=MyTendo.csv"},
    )
