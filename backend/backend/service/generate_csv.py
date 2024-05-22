import csv
import io
from typing import Any, Generator

from pydantic import BaseModel


# mypy doesn't work yet with cool new generics :(
def gen_csv[T: BaseModel](  # type: ignore[valid-type]
    lst: list[T],  # type: ignore[name-defined]
) -> Generator[Any, Any, Any]:
    output = io.StringIO()
    write = csv.writer(output)
    headers = lst[0].model_dump(exclude={"image"}).keys()
    write.writerow(headers)
    yield output.getvalue()
    output.seek(0)
    output.truncate(0)
    for game in lst:
        values = game.model_dump(exclude={"image"}).values()
        write.writerow(values)
        yield output.getvalue()
        output.seek(0)
        output.truncate(0)
