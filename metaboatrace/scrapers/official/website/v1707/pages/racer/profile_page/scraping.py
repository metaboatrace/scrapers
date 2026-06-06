import re
from datetime import date
from typing import IO

from bs4 import BeautifulSoup
from metaboatrace.models.racer import Racer, RacerRank
from metaboatrace.models.region import Branch, BranchFactory, PrefectureFactory

from metaboatrace.scrapers.official.website.v1707.decorators import no_content_handleable
from metaboatrace.scrapers.official.website.v1707.utils import select_one_or_raise


@no_content_handleable
def extract_racer_profile(file: IO[str]) -> Racer:
    soup = BeautifulSoup(file, "html.parser")

    full_name = select_one_or_raise(soup, ".racer1_bodyName").get_text()
    # 公式サイトは姓+名が長いと表示幅都合で区切りスペースを落とすことがある (例: toban=4011 堀之内紀代子).
    # 仮名側からの正確な漢字分割は復元不能なので、区切りが無い場合は姓に全体を入れて名は空文字にする.
    name_parts = re.split(r"[\s　]+", full_name, maxsplit=1)
    last_name = name_parts[0]
    first_name = name_parts[1] if len(name_parts) > 1 else ""

    dd_list = select_one_or_raise(soup, "dl.list3").select("dd")

    registration_number = int(dd_list[0].get_text())
    birth_date = date(*[int(ymd) for ymd in dd_list[1].get_text().split("/")])

    if m := re.match(r"(\d{3})cm", dd_list[2].get_text()):
        height = int(m.group(1))
    branch = Branch(BranchFactory.create(dd_list[5].get_text()))
    born_prefecture = PrefectureFactory.create(dd_list[6].get_text())
    if m := re.match(r"(\d{2,3})期", dd_list[7].get_text()):
        term = int(m.group(1))
    racer_rank = RacerRank.from_string(dd_list[8].get_text()[:2])

    return Racer(
        registration_number=registration_number,
        last_name=last_name,
        first_name=first_name,
        term=term,
        birth_date=birth_date,
        height=height,
        born_prefecture=born_prefecture,
        branch=branch,
        current_rating=racer_rank,
    )
