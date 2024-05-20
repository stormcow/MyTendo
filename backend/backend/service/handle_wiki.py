import asyncio
from typing import Any

import httpx
from bs4 import BeautifulSoup, Tag

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

client = httpx.AsyncClient(timeout=30, verify=False)


def get_image(soup: Tag) -> dict[str, Any]:
    s = soup.find(name="img")
    if isinstance(s, Tag):
        return {"image": s["src"]}
    else:
        return {"image": False}


def parse_game_info(game: httpx.Response) -> dict[str, Any]:
    soup = BeautifulSoup(game.content, "html.parser").find(
        name="table", class_="infobox"
    )
    if not soup:
        return {"infobox": False, "image": False}
    else:
        img = get_image(soup) if isinstance(soup, Tag) else {"image": False}
        img.update({"infobox": True})
        return img


async def fetch_game_details(game: dict[str, str]) -> dict[str, Any]:
    response = await client.get(
        url=f"https://en.wikipedia.org/w/index.php?curid={game['pageid']}"
    )
    game["response"] = str(response.status_code)
    extra_info = parse_game_info(response)
    game.update(extra_info)
    return game


async def get_all_games() -> list[dict[str, str]]:
    response = await client.get(url=URL, params=PARAMS)
    data = response.json()
    games: list[dict[str, str]] = []
    for cm in data["query"]["categorymembers"]:
        games.append(cm)

    tasks = [fetch_game_details(game) for game in games]
    await asyncio.gather(*tasks)
    tasks = []
    return games


async def main() -> None:
    games = await get_all_games()
    for game in games:
        print(game)


if __name__ == "__main__":
    asyncio.run(main())
