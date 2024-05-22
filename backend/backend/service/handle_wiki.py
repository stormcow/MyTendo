import asyncio
from typing import Any

import httpx
from bs4 import BeautifulSoup, Tag

from backend.schemas.game import GameSchemaTransit

URL = "https://en.wikipedia.org/w/api.php"
PARAMS = {
    "cmdir": "desc",
    "format": "json",
    "list": "categorymembers",
    "action": "query",
    "cmtitle": "Category:Nintendo_Switch-only_games",
    "cmsort": "timestamp",
    "cmlimit": "500",
}
QUESTION_MARK_IMAGE = "https://upload.wikimedia.org/wikipedia/commons/thumb/7/77/Question_mark-pixels.jpg/640px-Question_mark-pixels.jpg"

client = httpx.AsyncClient(timeout=30, verify=False)


def get_image(soup: Tag) -> dict[str, Any]:
    s = soup.find(name="img")
    if isinstance(s, Tag):
        return {"image": s["src"]}
    else:
        return {"image": QUESTION_MARK_IMAGE}


def parse_game_info(game: httpx.Response) -> dict[str, Any]:
    soup = BeautifulSoup(game.content, "html.parser").find(
        name="table", class_="infobox"
    )
    if not soup:
        return {"image": None}
    else:
        img = get_image(soup) if isinstance(soup, Tag) else {"image": None}
        return img


async def fetch_game_details(game: dict[str, Any]) -> GameSchemaTransit:
    response = await client.get(
        url=f"https://en.wikipedia.org/w/index.php?curid={game['pageid']}"
    )
    extra_info = parse_game_info(response)
    game.update(extra_info)
    return GameSchemaTransit(title=game["title"], image=game["image"])


async def get_all_games() -> list[GameSchemaTransit]:
    response = await client.get(url=URL, params=PARAMS)
    data = response.json()
    games: list[dict[str, str]] = []
    for cm in data["query"]["categorymembers"]:
        games.append(cm)

    tasks = [fetch_game_details(game) for game in games]
    return await asyncio.gather(*tasks)
