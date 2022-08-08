import re
from typing import IO

from boatrace.official.exceptions import DataNotFound
from bs4 import BeautifulSoup


def no_content_handleable(func):
    def wrapper(file: IO):
        soup = BeautifulSoup(file, "html.parser")

        if re.match(r"データ[がは]ありません", soup.select_one(".l-main").get_text().strip()):
            raise DataNotFound

        file.seek(0)
        return func(file)

    return wrapper
