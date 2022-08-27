from typing import IO, List

from boatrace.official.models import BoatPerformance
from boatrace.official.v1707.scrapers.decorators import no_content_handleable
from boatrace.official.v1707.scrapers.utils import parse_race_key_attributes
from bs4 import BeautifulSoup

PLACE_HOLDER_OF_UNRECORDED_DATA = "-"


@no_content_handleable
def scrape_boat_performance(file: IO) -> List[BoatPerformance]:
    soup = BeautifulSoup(file, "html.parser")
    race_key_attributes = parse_race_key_attributes(soup)

    data = []
    for _, row in enumerate(soup.select(".table1")[-1].select("tbody"), 1):
        data_strings = row.select_one("tr").select("td")[7].text.strip().split()
        number = int(data_strings[0])
        quinella_rate = (
            float(data_strings[1])
            if data_strings[1] != PLACE_HOLDER_OF_UNRECORDED_DATA
            else None
        )
        trio_rate = (
            float(data_strings[2])
            if data_strings[2] != PLACE_HOLDER_OF_UNRECORDED_DATA
            else None
        )

        data.append(
            BoatPerformance(
                recorded_date=race_key_attributes["race_holding_date"],
                number=number,
                quinella_rate=quinella_rate,
                trio_rate=trio_rate,
            )
        )

    return data
