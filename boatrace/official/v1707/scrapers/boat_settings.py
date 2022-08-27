from dataclasses import dataclass
from datetime import date
from typing import IO

from boatrace.models.stadium_tel_code import StadiumTelCode
from boatrace.official.exceptions import DataNotFound
from boatrace.official.v1707.scrapers.decorators import no_content_handleable
from boatrace.official.v1707.scrapers.utils import parse_race_key_attributes
from bs4 import BeautifulSoup


@dataclass(frozen=True)
class Dto:
    race_holding_date: date
    stadium_tel_code: StadiumTelCode
    race_number: int
    pit_number: int
    tilt: float
    is_new_propeller: bool


@no_content_handleable
def scrape_boat_settings(file: IO) -> Dto:
    NEW_PROPELLER_MARK = "新"

    soup = BeautifulSoup(file, "html.parser")
    race_key_attributes = parse_race_key_attributes(soup)
    race_holding_date = race_key_attributes["race_holding_date"]
    stadium_tel_code = race_key_attributes["stadium_tel_code"]
    race_number = race_key_attributes["race_number"]

    data = []

    for pit_number, row in enumerate(soup.select(".table1")[1].select("tbody"), 1):
        if "is-miss" in row["class"]:
            continue

        try:
            tilt = float(row.select("td")[5].text)
            is_new_propeller = row.select("td")[6].text.strip() == NEW_PROPELLER_MARK
        except ValueError:
            raise DataNotFound

        data.append(
            Dto(
                race_holding_date=race_holding_date,
                stadium_tel_code=stadium_tel_code,
                race_number=race_number,
                pit_number=pit_number,
                tilt=tilt,
                is_new_propeller=is_new_propeller,
            )
        )

    return data
