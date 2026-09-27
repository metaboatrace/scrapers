import io
import os
from datetime import date

import pytest
from metaboatrace.models.racer import Racer, RacerRank
from metaboatrace.models.region import Branch, Prefecture

from metaboatrace.scrapers.official.website.exceptions import DataNotFound
from metaboatrace.scrapers.official.website.v1707.pages.racer.profile_page.scraping import (
    extract_racer_profile,
)

base_path = os.path.dirname(os.path.abspath(__file__))


def test_extract_racer_profile() -> None:
    file_path = os.path.normpath(os.path.join(base_path, "./fixtures/4444.html"))

    with open(file_path) as file:
        data = extract_racer_profile(file)

    assert data == Racer(
        registration_number=4444,
        last_name="桐生",
        first_name="順平",
        term=100,
        birth_date=date(1986, 10, 7),
        height=162,
        born_prefecture=Prefecture.FUKUSHIMA,
        branch=Branch.SAITAMA,
        current_rating=RacerRank.A1,
    )


def test_extract_racer_profile_when_name_has_no_separator_space() -> None:
    # 公式サイトは姓+名が長い場合に表示幅都合でスペースを落とすことがある (toban=4011 堀之内紀代子).
    # 仮名から漢字分割は復元できないので姓側に全体を寄せ、名は空文字で返す.
    file_path = os.path.normpath(os.path.join(base_path, "./fixtures/4011.html"))

    with open(file_path) as file:
        data = extract_racer_profile(file)

    assert data == Racer(
        registration_number=4011,
        last_name="堀之内紀代子",
        first_name="",
        term=84,
        birth_date=date(1979, 9, 9),
        height=158,
        born_prefecture=Prefecture.OKAYAMA,
        branch=Branch.OKAYAMA,
        current_rating=RacerRank.A1,
    )


def test_extract_racer_profile_of_rookie_before_debut() -> None:
    # デビュー前の新人は出身地・血液型が空欄のまま公開される (toban=5493 松尾青波, 139 期,
    # 2026-09-27 取得)。任意項目の空欄は None として、氏名・登録期・支部は取得できること。
    file_path = os.path.normpath(os.path.join(base_path, "./fixtures/5493.html"))

    with open(file_path) as file:
        data = extract_racer_profile(file)

    assert data == Racer(
        registration_number=5493,
        last_name="松尾",
        first_name="青波",
        term=139,
        birth_date=date(2007, 3, 5),
        height=172,
        born_prefecture=None,
        branch=Branch.NAGASAKI,
        current_rating=RacerRank.B2,
    )


def _rookie_html_with(dd_before: str, dd_after: str) -> str:
    """5493 fixture の 1 セルだけ差し替えた HTML を返す (欠損・表記変更のシミュレーション)."""
    file_path = os.path.normpath(os.path.join(base_path, "./fixtures/5493.html"))
    with open(file_path) as file:
        html = file.read()
    assert html.count(dd_before) == 1, f"fixture に {dd_before!r} が一意に存在すること"
    return html.replace(dd_before, dd_after)


def test_blank_term_and_height_are_none() -> None:
    # 任意項目は空欄なら None。登録期が空欄でもレコードは捨てない (欠損は crawlers 側の
    # 補完対象判定で拾う)。
    html = _rookie_html_with("<dd>139期</dd>", "<dd></dd>").replace("<dd>172cm</dd>", "<dd> </dd>")

    data = extract_racer_profile(io.StringIO(html))

    assert data.term is None
    assert data.height is None


@pytest.mark.parametrize(
    ("before", "after"),
    [
        ("<dd>139期</dd>", "<dd>第139期</dd>"),
        ("<dd>172cm</dd>", "<dd>172 cm</dd>"),
    ],
)
def test_unknown_format_is_not_silently_none(before: str, after: str) -> None:
    # 空欄だけを許容し、非空欄の表記変更は ValueError で検知する (None に潰さない)。
    with pytest.raises(ValueError, match=r"unexpected .* format"):
        extract_racer_profile(io.StringIO(_rookie_html_with(before, after)))


def test_scrape_a_no_contents_page() -> None:
    file_path = os.path.normpath(
        os.path.join(os.path.join(base_path, "./fixtures/data_not_found.html"))
    )

    with open(file_path) as file, pytest.raises(DataNotFound):
        extract_racer_profile(file)
