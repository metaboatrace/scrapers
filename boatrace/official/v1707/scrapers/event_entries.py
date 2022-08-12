import re
from typing import IO, List

from boatrace.models.gender import Gender
from boatrace.models.racer_rank import RacerRank
from boatrace.official.models import EventEntry
from boatrace.official.v1707.scrapers.decorators import no_content_handleable
from bs4 import BeautifulSoup


@no_content_handleable
def scrape_pre_inspection_information(file: IO) -> List[EventEntry]:
    """前検情報をスクレイピングする

    Args:
        file (IO): 前検情報のHTML

    Raises:
        DataNotFound:

    Returns:
        List[EventEntry]: パース結果を保持するデータモデルのコレクション
    """
    soup = BeautifulSoup(file, "html.parser")

    data = []
    series_entry_rows = soup.select(".table1 table tbody tr")
    pattern_of_name_delimiter = re.compile(r"[　]+")

    for row in series_entry_rows:
        cells = row.select("td")
        try:
            racer_last_name, racer_first_name = pattern_of_name_delimiter.split(
                cells[2].get_text().strip()
            )
        except ValueError:
            racer_last_name = cells[2].get_text()
            racer_first_name = ""

        data.append(
            EventEntry(
                racer_registration_number=int(cells[1].get_text()),
                racer_last_name=racer_last_name,
                racer_first_name=racer_first_name,
                racer_rank=RacerRank(cells[3].get_text().strip()),
                motor_number=int(cells[4].get_text()),
                quinella_rate_of_motor=float(cells[5].get_text().replace("%", "")),
                boat_number=int(cells[6].get_text()),
                quinella_rate_of_boat=float(cells[7].get_text().replace("%", "")),
                anterior_time=float(cells[8].get_text().replace("%", "")),
                racer_gender=Gender.FEMALE
                if row.select_one("i.is-lady")
                else Gender.MALE,
            )
        )

    return data
