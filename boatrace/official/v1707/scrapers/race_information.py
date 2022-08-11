import re
from datetime import date, datetime
from operator import itemgetter
from typing import IO
from urllib.parse import parse_qs, urlparse

from boatrace.models.race_laps import RaceLapsFactory
from boatrace.models.stadium_tel_code import StadiumTelCode
from boatrace.official.exceptions import ScrapingError
from boatrace.official.models import RaceInformation
from boatrace.official.v1707.scrapers.decorators import no_content_handleable
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
    todays_race_list_url = soup.select_one(
        "body > div.l-header > ul > li:nth-child(3) > a"
    )["href"]
    stadiutm_tel_codes, dates = itemgetter("jcd", "hd")(
        parse_qs(urlparse(todays_race_list_url).query)
    )

    if len(stadiutm_tel_codes) != 1 or len(dates) != 1:
        raise ScrapingError

    stadiutm_tel_code = StadiumTelCode(int(stadiutm_tel_codes[0]))
    date_string = dates[0]
    race_holding_date = date(
        int(date_string[:4]), int(date_string[4:6]), int(date_string[6:])
    )

    deadline_table = soup.select_one(".table1")
    deadline_table.select_one("tr th:not([class])").text
    if m := re.match(
        r"(\d{1,2})R", deadline_table.select_one("tr th:not([class])").text
    ):
        number = int(m.group(1))
    else:
        raise ScrapingError

    deadline_text = (
        deadline_table.select("tbody tr")[-1].select("td")[number].get_text()
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
        stadium_tel_code=stadiutm_tel_code,
        number=number,
        title=title,
        race_laps=RaceLapsFactory.create(metre),
        deadline_at=deadline_at,
        is_course_fixed="進入固定" in soup.body.get_text(),
        use_stabilizer="安定板使用" in soup.body.get_text(),
    )
