from dataclasses import dataclass
from datetime import date
from typing import IO, List

from boatrace.models.motor_parts import MotorParts, MotorPartsFactory
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
    motor_parts_exchanges: List[tuple[MotorParts, int]]


@no_content_handleable
def scrape_boat_settings(file: IO) -> Dto:
    NEW_PROPELLER_MARK = "新"
    MOTOR_PARTS_QUANTITY_DELIMITER = "×"

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

        numbers = dict(zip(["１", "２", "３", "４", "５", "６", "７", "８", "９"], range(1, 10)))
        motor_parts_exchanges = []
        for li in row.select("td")[7].select("li"):
            if MOTOR_PARTS_QUANTITY_DELIMITER in li.get_text():
                parts_name, quantity_text = li.get_text().split(
                    MOTOR_PARTS_QUANTITY_DELIMITER
                )
            else:
                parts_name = li.get_text()
                quantity_text = None

            motor_parts_exchanges.append(
                (MotorPartsFactory.create(parts_name), numbers.get(quantity_text, 1))
            )

        data.append(
            Dto(
                race_holding_date=race_holding_date,
                stadium_tel_code=stadium_tel_code,
                race_number=race_number,
                pit_number=pit_number,
                tilt=tilt,
                is_new_propeller=is_new_propeller,
                motor_parts_exchanges=motor_parts_exchanges,
            )
        )

    return data
