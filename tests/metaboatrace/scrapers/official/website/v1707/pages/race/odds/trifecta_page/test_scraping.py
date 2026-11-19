import io
from datetime import UTC, date, datetime
from pathlib import Path

import pytest
from metaboatrace.models.race import BettingMethod, Odds
from metaboatrace.models.stadium import StadiumTelCode

from metaboatrace.scrapers.official.website.exceptions import (
    DataNotFound,
    RaceCanceled,
    ScrapingError,
)
from metaboatrace.scrapers.official.website.v1707.pages.race.odds.trifecta_page.scraping import (
    OddsPageState,
    OddsPageStatus,
    extract_odds,
    extract_odds_page_state,
)

FIXTURE_DIR = Path(__file__).parent / "fixtures"


def test_extract_odds() -> None:
    file_path = FIXTURE_DIR / "20170919_19#_11R.html"

    with open(file_path) as file:
        data = extract_odds(file)

    assert len(data) == 60
    assert data[0] == Odds(
        race_holding_date=date(2017, 9, 19),
        stadium_tel_code=StadiumTelCode.SHIMONOSEKI,
        race_number=11,
        betting_method=BettingMethod.TRIFECTA,
        betting_numbers=[1, 2, 3],
        ratio=6.1,
    )
    assert data[-1] == Odds(
        race_holding_date=date(2017, 9, 19),
        stadium_tel_code=StadiumTelCode.SHIMONOSEKI,
        race_number=11,
        betting_method=BettingMethod.TRIFECTA,
        betting_numbers=[5, 4, 3],
        ratio=413.5,
    )
    assert len([odds for odds in data if "6" in str(odds.betting_numbers)]) == 0


def test_extarct_odds_from_a_no_contents_page() -> None:
    file_path = FIXTURE_DIR / "20170102_01#_1R.html"

    with open(file_path) as file, pytest.raises(DataNotFound):
        extract_odds(file)


def test_extract_odds_from_a_canceled_race() -> None:
    file_path = FIXTURE_DIR / "20180103_03#_11R.html"

    with open(file_path) as file, pytest.raises(RaceCanceled):
        extract_odds(file)


def test_extract_odds_from_a_page_showing_the_update_time() -> None:
    file_path = FIXTURE_DIR / "20261119_15#_12R_before_deadline.html"

    with open(file_path) as file:
        data = extract_odds(file)

    assert len(data) == 120
    assert data[0].race_holding_date == date(2026, 11, 19)
    assert data[0].stadium_tel_code == StadiumTelCode.MARUGAME
    assert data[0].race_number == 12
    assert data[0].betting_numbers == [1, 2, 3]


def test_extract_odds_page_state_from_a_page_showing_the_update_time() -> None:
    # 締切 20:45 のレースを 20:42 に取得したページ。表示は「オッズ更新時間 20:41」
    file_path = FIXTURE_DIR / "20261119_15#_12R_before_deadline.html"

    with open(file_path) as file:
        state = extract_odds_page_state(file)

    assert state == OddsPageState(
        status=OddsPageStatus.PROVISIONAL,
        odds_updated_at=datetime(2026, 11, 19, 11, 41, tzinfo=UTC),
    )


def test_extract_odds_page_state_stays_provisional_just_after_the_deadline() -> None:
    # 同じレースを締切 20 秒後の 20:45:20 に取得したページ。締切を過ぎていても、集計が
    # 終わるまでは「オッズ更新時間 20:44」のままで、確定の表示にはなっていない
    file_path = FIXTURE_DIR / "20261119_15#_12R_just_after_deadline.html"

    with open(file_path) as file:
        state = extract_odds_page_state(file)

    assert state == OddsPageState(
        status=OddsPageStatus.PROVISIONAL,
        odds_updated_at=datetime(2026, 11, 19, 11, 44, tzinfo=UTC),
    )


@pytest.mark.parametrize(
    "fixture_name",
    [
        pytest.param("20170919_19#_11R.html", id="2017 markup"),
        # 同じレースを締切 80 秒後の 20:46:20 に取得したページ
        pytest.param("20261119_15#_12R_final.html", id="2026 markup, 80s after the deadline"),
    ],
)
def test_extract_odds_page_state_from_a_page_showing_final_odds(fixture_name: str) -> None:
    with open(FIXTURE_DIR / fixture_name) as file:
        state = extract_odds_page_state(file)

    assert state == OddsPageState(status=OddsPageStatus.FINAL, odds_updated_at=None)


def test_extract_odds_page_state_from_a_no_contents_page() -> None:
    file_path = FIXTURE_DIR / "20170102_01#_1R.html"

    with open(file_path) as file, pytest.raises(DataNotFound):
        extract_odds_page_state(file)


def test_extract_odds_page_state_from_a_canceled_race() -> None:
    file_path = FIXTURE_DIR / "20180103_03#_11R.html"

    with open(file_path) as file, pytest.raises(RaceCanceled):
        extract_odds_page_state(file)


def _provisional_page_with_refresh_text(replacement: str) -> io.StringIO:
    html = (FIXTURE_DIR / "20261119_15#_12R_before_deadline.html").read_text()
    marker = "オッズ更新時間"
    assert html.count(marker) == 1
    start = html.index(marker)
    end = html.index("</p>", start)
    return io.StringIO(html[:start] + replacement + html[end:])


def test_extract_odds_page_state_keeps_the_status_when_the_update_time_is_blank() -> None:
    file = _provisional_page_with_refresh_text("オッズ更新時間\n&nbsp;\n")

    assert extract_odds_page_state(file) == OddsPageState(
        status=OddsPageStatus.PROVISIONAL, odds_updated_at=None
    )


def test_extract_odds_page_state_rejects_a_page_without_either_label() -> None:
    # 段階を示す表示が無いページを暫定 / 確定のどちらかに倒さない
    file = _provisional_page_with_refresh_text("")

    with pytest.raises(ScrapingError):
        extract_odds_page_state(file)
