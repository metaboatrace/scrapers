import re
from datetime import date
from typing import IO

from boatrace.models.branch import Branch
from boatrace.models.prefecture import PrefectureFactory
from boatrace.models.racer_rank import RacerRank
from boatrace.official.models import Racer
from boatrace.official.v1707.scrapers.decorators import no_content_handleable
from bs4 import BeautifulSoup


@no_content_handleable
def scrape_racer_profile(file: IO) -> Racer:
    """レーサーのプロフィールをスクレイピングする

    Args:
        file (IO): レーサープロフィールのHTML

    Raises:
        DataNotFound:
        ScrapingError:

    Returns:
        Racer: パース結果を保持するデータモデル
    """
    soup = BeautifulSoup(file, "html.parser")

    full_name = soup.select_one(".racer1_bodyName").get_text()
    last_name, first_name = re.split(r"[\s　]+", full_name)

    dd_list = soup.select_one("dl.list3").select("dd")

    registration_number = int(dd_list[0].get_text())
    birth_date = date(*[int(ymd) for ymd in dd_list[1].get_text().split("/")])

    if m := re.match(r"(\d{3})cm", dd_list[2].get_text()):
        height = int(m.group(1))
    if m := re.match(r"(\d{2})kg", dd_list[3].get_text()):
        weight = int(m.group(1))
    branch_prefecture = Branch(PrefectureFactory.create(dd_list[5].get_text()))
    born_prefecture = PrefectureFactory.create(dd_list[6].get_text())
    if m := re.match(r"(\d{2,3})期", dd_list[7].get_text()):
        term = int(m.group(1))
    racer_rank = RacerRank(dd_list[8].get_text()[:2])

    return Racer(
        last_name=last_name,
        first_name=first_name,
        registration_number=registration_number,
        birth_date=birth_date,
        height=height,
        weight=weight,
        branch_prefecture=branch_prefecture,
        born_prefecture=born_prefecture,
        term=term,
        current_rating=racer_rank,
    )
