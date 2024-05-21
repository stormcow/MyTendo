from sqlalchemy import insert
from sqlalchemy.orm import Session

from ..models.game import Game
from ..schemas.game import GameSchemaTransit


class GameInterface:
    def insert_game(self, game: GameSchemaTransit, session: Session) -> Game | None:
        with session as s:
            result = s.execute(insert(Game).returning(Game), game.model_dump()).scalar()

        return result if isinstance(result, Game) else None

    def insert_games(
        self, games: list[GameSchemaTransit], session: Session
    ) -> list[Game] | None:
        with session as s:
            result = (
                s.execute(
                    insert(Game).returning(Game), [game.model_dump() for game in games]
                )
                .scalars()
                .all()
            )

        return result if isinstance(result, list) else None
