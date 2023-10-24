import httpx

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

client = httpx.AsyncClient()


async def get_all_games() -> list[dict[str, str]]:
    response = await client.get(url=URL, params=PARAMS)
    data = response.json()
    games: list[dict[str, str]] = []
    for cm in data["query"]["categorymembers"]:
        games.append(cm)
    return games
