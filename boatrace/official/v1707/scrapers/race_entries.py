import re
from typing import IO, List

from boatrace.models.racer_rank import RacerRank
from boatrace.official.exceptions import ScrapingError
from boatrace.official.models import RaceEntry
from boatrace.official.v1707.scrapers.decorators import no_content_handleable
from boatrace.official.v1707.scrapers.utils import parse_race_key_attributes
from bs4 import BeautifulSoup


@no_content_handleable
def scrape_race_entries(file: IO) -> List[RaceEntry]:
    soup = BeautifulSoup(file, "html.parser")
    race_key_attributes = parse_race_key_attributes(soup)

    data = []
    for pit_number, row in enumerate(soup.select(".table1")[-1].select("tbody"), 1):
        racer_photo_path = row.select_one("tr").select("td")[1].select_one("img")["src"]
        if m := re.search(r"(\d+)\.jpe?g$", racer_photo_path):
            racer_registration_number = int(m.group(1))
        else:
            raise ScrapingError

        racer_full_name = (
            row.select_one("tr").select("td")[2].select_one("a").text.strip()
        )
        racer_last_name, racer_first_name = re.split(r"[　 ]+", racer_full_name)

        racer_rank = RacerRank(
            row.select_one("tr").select("td")[2].select_one("span").text.strip()
        )

        motor_number = int(row.select_one("tr").select("td")[6].text.strip().split()[0])
        boat_number = int(row.select_one("tr").select("td")[7].text.strip().split()[0])

        is_absent = "is-miss" in row["class"]

        data.append(
            RaceEntry(
                **race_key_attributes,
                racer_registration_number=racer_registration_number,
                racer_last_name=racer_last_name,
                racer_first_name=racer_first_name,
                pit_number=pit_number,
                current_racer_rating=racer_rank,
                is_absent=is_absent,
                motor_number=motor_number,
                boat_number=boat_number,
            )
        )

    return data
