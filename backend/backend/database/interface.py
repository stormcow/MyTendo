from sqlalchemy import insert, select, update
from sqlalchemy.orm import Session

from ..models.game import Game
from ..schemas.game import GameSchema, GameSchemaTransit


class GameInterface:
    def insert_game(self, game: GameSchemaTransit, session: Session) -> Game | None:
        with session as s:
            result = s.execute(insert(Game).returning(Game), game.model_dump()).scalar()

        return result if isinstance(result, Game) else None

    def insert_games(
        self, games: list[GameSchemaTransit], session: Session
    ) -> list[Game] | None:
        with session as s:
            s.execute(
                insert(Game),
                [game.model_dump() for game in games if not self.get_game(s, game)],
            )
            s.commit()
            result = s.execute(select(Game)).scalars().fetchall()
        return list(result) if result else None

    def get_games(self, session: Session) -> list[Game] | None:
        with session as s:
            result = s.execute(select(Game)).scalars().fetchall()
        return list(result) if result else None

    def get_game(
        self, session: Session, game: GameSchemaTransit | GameSchema | int
    ) -> Game | None:
        with session as s:
            if isinstance(game, GameSchema):
                result = s.execute(select(Game).where(Game.id == game.id)).scalar()
            elif isinstance(game, int):
                result = s.execute(select(Game).where(Game.id == game)).scalar()
            elif isinstance(game, GameSchemaTransit):
                result = s.execute(
                    select(Game).where(Game.title == game.title)
                ).scalar()
        return result

    def update_game(self, session: Session, game: GameSchema) -> Game | None:
        with session as s:
            s.execute(
                update(Game)
                .where(Game.id == game.id)
                .values(game.model_dump(exclude={"id"}))
            )
            s.commit()
            result = self.get_game(s, game)

        return result

    def update_games(
        self, session: Session, games: list[GameSchema]
    ) -> list[Game] | None:
        with session as s:
            [self.update_game(s, game) for game in games if self.get_game(s, game)]
            s.commit()
            result = [self.get_game(s, game) for game in games]
        return [game for game in result if game]
