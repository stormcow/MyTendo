from pydantic import BaseModel, ConfigDict


class Base(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int


class GameSchemaTransit(BaseModel):
    title: str
    image: str | None = None
    owned: bool = False


class GameSchema(GameSchemaTransit, Base):
    pass
