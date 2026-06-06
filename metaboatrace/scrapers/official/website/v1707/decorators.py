import re
from collections.abc import Callable
from typing import IO

from bs4 import BeautifulSoup

from metaboatrace.scrapers.official.website.exceptions import DataNotFound, RaceCanceled
from metaboatrace.scrapers.official.website.v1707.utils import select_one_or_raise


def no_content_handleable[R](func: Callable[[IO[str]], R]) -> Callable[[IO[str]], R]:
    def wrapper(file: IO[str]) -> R:
        soup = BeautifulSoup(file, "html.parser")

        if re.match(
            r"データ[がは]ありません", select_one_or_raise(soup, ".l-main").get_text().strip()
        ):
            raise DataNotFound

        body_text = select_one_or_raise(soup, "body").get_text()
        if "※ データはありません。" in body_text:
            raise DataNotFound

        if "※ データが存在しないのでページを表示できません。" in body_text:
            raise DataNotFound

        file.seek(0)
        return func(file)

    return wrapper


def race_cancellation_handleable[R](func: Callable[[IO[str]], R]) -> Callable[[IO[str]], R]:
    def wrapper(file: IO[str]) -> R:
        soup = BeautifulSoup(file, "html.parser")

        if re.search(r"レース[は]?中止", select_one_or_raise(soup, ".l-main").get_text().strip()):
            raise RaceCanceled

        file.seek(0)
        return func(file)

    return wrapper
