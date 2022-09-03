import re
from dataclasses import dataclass
from datetime import date
from typing import IO, List

from boatrace.official.v1707.scrapers.decorators import (
    no_content_handleable,
    race_cancellation_handleable,
)
from boatrace.official.v1707.scrapers.utils import parse_race_key_attributes
from bs4 import BeautifulSoup


@dataclass(frozen=True)
class Dto:
    recorded_on: date
    racer_registration_number: int
    weight: int
    adjust: float


@no_content_handleable
@race_cancellation_handleable
def scrape_racer_conditions(file: IO) -> List[Dto]:
    soup = BeautifulSoup(file, "html.parser")

    # hack: 欲しいのは日付だけで場コードと何レース目かは不要なんだけどいったんこれで
    race_key_attributes = parse_race_key_attributes(soup)

    data = []
    for row in soup.select(".table1")[1].select("tbody"):
        if "is-miss" in row["class"]:
            # 欠場
            continue

        if m := re.search(
            r"toban=(\d{4})$", row.select("td")[2].select_one("a")["href"]
        ):
            racer_registration_number = int(m.group(1))
        else:
            raise ValueError

        weight = float(row.select("td")[3].text[:-2])
        adjust = float(row.select("td")[12].text)

        data.append(
            Dto(
                recorded_on=race_key_attributes["race_holding_date"],
                racer_registration_number=racer_registration_number,
                weight=weight,
                adjust=adjust,
            )
        )

    return data
