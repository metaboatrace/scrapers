import re
from datetime import datetime
from typing import IO

from boatrace.models.race_laps import RaceLapsFactory
from boatrace.official.exceptions import ScrapingError
from boatrace.official.models import RaceInformation
from boatrace.official.v1707.scrapers.decorators import no_content_handleable
from boatrace.official.v1707.scrapers.utils import parse_race_key_attributes
from bs4 import BeautifulSoup


@no_content_handleable
def scrape_race_information(file: IO) -> RaceInformation:
    """レース情報をスクレイピングする

    Args:
        file (IO): 出走表のHTML

    Raises:
        ScrapingError:
        DataNotFound:

    Returns:
        RaceInformation: パース結果を保持するデータモデル
    """
    soup = BeautifulSoup(file, "html.parser")
    race_key_attributes = parse_race_key_attributes(soup)
    race_holding_date = race_key_attributes["race_holding_date"]
    stadium_tel_code = race_key_attributes["stadium_tel_code"]
    race_number = race_key_attributes["race_number"]

    deadline_table = soup.select_one(".table1")
    deadline_text = (
        deadline_table.select("tbody tr")[-1].select("td")[race_number].get_text()
    )
    hour, minute = [int(t) for t in deadline_text.split(":")]
    deadline_at = datetime(
        race_holding_date.year,
        race_holding_date.month,
        race_holding_date.day,
        hour,
        minute,
    )

    if m := re.match(
        r"(\w+)\s*(1200|1800)m",
        soup.select_one("h3.title16_titleDetail__add2020").get_text().strip(),
    ):
        title = m.group(1)
        metre = int(m.group(2))
    else:
        raise ScrapingError

    return RaceInformation(
        date=race_holding_date,
        stadium_tel_code=stadium_tel_code,
        number=race_number,
        title=title,
        race_laps=RaceLapsFactory.create(metre),
        deadline_at=deadline_at,
        is_course_fixed="進入固定" in soup.body.get_text(),
        use_stabilizer="安定板使用" in soup.body.get_text(),
    )
