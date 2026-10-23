import re
from datetime import date
from typing import IO

from bs4 import BeautifulSoup
from metaboatrace.models.racer import Racer, RacerRank
from metaboatrace.models.region import Branch, BranchFactory, PrefectureFactory

from metaboatrace.scrapers.official.website.v1707.decorators import no_content_handleable
from metaboatrace.scrapers.official.website.v1707.utils import (
    select_one_or_raise,
    split_racer_name,
)


def _optional_int(text: str, pattern: str, label: str) -> int | None:
    """任意の数値項目を読む: 空欄は None、非空欄は ``pattern`` に一致しなければ ValueError.

    「空欄だけを許容し、表記の変更は検知する」を 1 箇所で保証する。空欄と形式不一致を
    同じ None に潰すと、公式サイトの表記変更で欠損が無検知のまま蓄積するため分ける。
    """
    stripped = text.strip()
    if not stripped:
        return None
    if m := re.match(pattern, stripped):
        return int(m.group(1))
    raise ValueError(f"unexpected {label} format: {stripped!r}")


@no_content_handleable
def extract_racer_profile(file: IO[str]) -> Racer:
    soup = BeautifulSoup(file, "html.parser")

    last_name, first_name = split_racer_name(
        select_one_or_raise(soup, ".racer1_bodyName").get_text()
    )

    dd_list = select_one_or_raise(soup, "dl.list3").select("dd")

    registration_number = int(dd_list[0].get_text())
    birth_date = date(*[int(ymd) for ymd in dd_list[1].get_text().split("/")])

    # デビュー前の新人 (養成所卒業直後〜初出走まで) はプロフィールが部分的にしか公開されず、
    # 出身地・血液型が空欄になる (例: toban=5493, 2026-09 時点の 139 期全員)。任意項目の空欄で
    # レコード全体 (氏名・登録期・支部) を捨てないよう、空欄は None にする。空欄ではない未知の
    # 文字列はこれまで通り ValueError にして、サイト側の表記変更に気づけるようにする。
    height = _optional_int(dd_list[2].get_text(), r"(\d{3})cm", "height")
    branch_text = dd_list[5].get_text().strip()
    branch = Branch(BranchFactory.create(branch_text)) if branch_text else None
    prefecture_text = dd_list[6].get_text().strip()
    born_prefecture = PrefectureFactory.create(prefecture_text) if prefecture_text else None
    term = _optional_int(dd_list[7].get_text(), r"(\d{2,3})期", "term")
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
