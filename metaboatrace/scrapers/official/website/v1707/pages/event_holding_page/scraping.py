import re
from typing import IO, Optional, Union

from bs4 import BeautifulSoup
from metaboatrace.models.stadium import StadiumTelCode

CANCELED_TEXTS = ["中止順延", "中止"]


def extract_event_holdings(file: IO[str]) -> list[dict[str, Union[StadiumTelCode, str]]]:
    soup = BeautifulSoup(file, "html.parser")

    data = []
    for tbody in soup.select(".table1 table tbody"):
        text = tbody.get_text()
        html_string = str(tbody)
        data.append(
            {
                "stadium_tel_code": _stadium_tel_code(html_string),
                "day_text": _cancel_text(text) if _canceled(text) else _day_text(text),
            }
        )

    return data


def _canceled(text: str) -> bool:
    if re.search(r"\d+R以降中止", text):
        return False
    return any(ct in text for ct in CANCELED_TEXTS)


def _cancel_text(text: str) -> Optional[str]:
    if re.search(r"\d+R以降中止", text):
        return None
    for ct in CANCELED_TEXTS:
        if ct in text:
            return ct
    return None


def _stadium_tel_code(html_string: str) -> StadiumTelCode:
    match = re.search(r"\?jcd=(\d{2})", html_string)
    if not match:
        raise ValueError("Invalid file format")
    return StadiumTelCode(int(match.group(1)))


def _day_text(text: str) -> Optional[str]:
    match = re.search(r"(初日|[\d１２３４５６７]日目|最終日)", text)
    return match.group(0) if match else None
