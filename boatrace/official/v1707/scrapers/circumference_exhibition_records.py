import re
from dataclasses import dataclass
from datetime import date
from typing import IO, List

from boatrace.models.stadium_tel_code import StadiumTelCode
from boatrace.official.v1707.scrapers.decorators import (
    no_content_handleable,
    race_cancellation_handleable,
)
from boatrace.official.v1707.scrapers.utils import parse_race_key_attributes
from bs4 import BeautifulSoup


@dataclass(frozen=True)
class Dto:
    race_holding_date: date
    stadium_tel_code: StadiumTelCode
    race_number: int
    pit_number: int
    exhibition_time: float


@no_content_handleable
@race_cancellation_handleable
def scrape_circumference_exhibition_records(file: IO) -> List[Dto]:
    soup = BeautifulSoup(file, "html.parser")
    race_key_attributes = parse_race_key_attributes(soup)

    data = []
    for pit_number, row in enumerate(soup.select(".table1")[1].select("tbody"), 1):
        if "is-miss" in row["class"]:
            # 欠場
            continue

        try:
            exhibition_time = float(row.select("td")[4].text)
        except TypeError:
            # 欠場じゃなくても展示だけ不参加とか展示中に転覆とかだとNoneをfloatで評価した結果ここに来るかも？
            continue

        data.append(
            Dto(
                **race_key_attributes,
                pit_number=pit_number,
                exhibition_time=exhibition_time,
            )
        )

    return data
