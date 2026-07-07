import os

from metaboatrace.models.stadium import EventHolding, EventHoldingStatus, StadiumTelCode

from metaboatrace.scrapers.official.website.v1707.pages.event_holding_page.scraping import (
    extract_event_holdings,
)

base_path = os.path.dirname(os.path.abspath(__file__))


def test_scrape_event_holdings_with_cancellations_and_delays() -> None:
    file_path = os.path.normpath(os.path.join(base_path, "./fixtures/2015_08_25.html"))
    with open(file_path) as file:
        data = extract_event_holdings(file)

    expected_results = [
        EventHolding(
            stadium_tel_code=StadiumTelCode.EDOGAWA,
            date=None,
            status=EventHoldingStatus.OPEN,
            progress_day=3,
        ),
        EventHolding(
            stadium_tel_code=StadiumTelCode.HEIWAJIMA,
            date=None,
            status=EventHoldingStatus.OPEN,
            progress_day=-1,
        ),
        EventHolding(
            stadium_tel_code=StadiumTelCode.GAMAGORI,
            date=None,
            status=EventHoldingStatus.OPEN,
            progress_day=1,
        ),
        EventHolding(
            stadium_tel_code=StadiumTelCode.BIWAKO,
            date=None,
            status=EventHoldingStatus.OPEN,
            progress_day=5,
        ),
        EventHolding(
            stadium_tel_code=StadiumTelCode.KOJIMA,
            date=None,
            status=EventHoldingStatus.POSTPONED,
            progress_day=None,
        ),
        EventHolding(
            stadium_tel_code=StadiumTelCode.TOKUYAMA,
            date=None,
            status=EventHoldingStatus.POSTPONED,
            progress_day=None,
        ),
        EventHolding(
            stadium_tel_code=StadiumTelCode.SHIMONOSEKI,
            date=None,
            status=EventHoldingStatus.CANCELED,
            progress_day=None,
        ),
        EventHolding(
            stadium_tel_code=StadiumTelCode.WAKAMATSU,
            date=None,
            status=EventHoldingStatus.POSTPONED,
            progress_day=None,
        ),
        EventHolding(
            stadium_tel_code=StadiumTelCode.FUKUOKA,
            date=None,
            status=EventHoldingStatus.POSTPONED,
            progress_day=None,
        ),
        EventHolding(
            stadium_tel_code=StadiumTelCode.KARATSU,
            date=None,
            status=EventHoldingStatus.POSTPONED,
            progress_day=None,
        ),
        EventHolding(
            stadium_tel_code=StadiumTelCode.OMURA,
            date=None,
            status=EventHoldingStatus.CANCELED,
            progress_day=None,
        ),
    ]

    for expected, actual in zip(expected_results, data, strict=True):
        assert actual.stadium_tel_code == expected.stadium_tel_code
        assert actual.date == expected.date
        assert actual.status == expected.status
        assert actual.progress_day == expected.progress_day


def test_scrape_event_holdings_with_postponements_after_nth_race() -> None:
    file_path = os.path.normpath(os.path.join(base_path, "./fixtures/2020_08_13.html"))
    with open(file_path) as file:
        data = extract_event_holdings(file)

    expected_results = [
        EventHolding(
            stadium_tel_code=StadiumTelCode.KIRYU,
            date=None,
            status=EventHoldingStatus.OPEN,
            progress_day=1,
        ),
        EventHolding(
            stadium_tel_code=StadiumTelCode.TODA,
            date=None,
            status=EventHoldingStatus.OPEN,
            progress_day=3,
        ),
        EventHolding(
            stadium_tel_code=StadiumTelCode.EDOGAWA,
            date=None,
            status=EventHoldingStatus.OPEN,
            progress_day=1,
        ),
        EventHolding(
            stadium_tel_code=StadiumTelCode.HAMANAKO,
            date=None,
            status=EventHoldingStatus.OPEN,
            progress_day=1,
        ),
        EventHolding(
            stadium_tel_code=StadiumTelCode.GAMAGORI,
            date=None,
            status=EventHoldingStatus.OPEN,
            progress_day=1,
        ),
        EventHolding(
            stadium_tel_code=StadiumTelCode.MIKUNI,
            date=None,
            status=EventHoldingStatus.OPEN,
            progress_day=-1,
        ),
        EventHolding(
            stadium_tel_code=StadiumTelCode.BIWAKO,
            date=None,
            status=EventHoldingStatus.OPEN,
            progress_day=-1,
        ),
        EventHolding(
            stadium_tel_code=StadiumTelCode.SUMINOE,
            date=None,
            status=EventHoldingStatus.CANCELED,
            progress_day=None,
        ),
        EventHolding(
            stadium_tel_code=StadiumTelCode.AMAGASAKI,
            date=None,
            status=EventHoldingStatus.OPEN,
            progress_day=5,
        ),
        EventHolding(
            stadium_tel_code=StadiumTelCode.NARUTO,
            date=None,
            status=EventHoldingStatus.OPEN,
            progress_day=3,
        ),
        EventHolding(
            stadium_tel_code=StadiumTelCode.MIYAJIMA,
            date=None,
            status=EventHoldingStatus.OPEN,
            progress_day=2,
        ),
        EventHolding(
            stadium_tel_code=StadiumTelCode.TOKUYAMA,
            date=None,
            status=EventHoldingStatus.OPEN,
            progress_day=1,
        ),
        EventHolding(
            stadium_tel_code=StadiumTelCode.WAKAMATSU,
            date=None,
            status=EventHoldingStatus.OPEN,
            progress_day=4,
        ),
        EventHolding(
            stadium_tel_code=StadiumTelCode.FUKUOKA,
            date=None,
            status=EventHoldingStatus.OPEN,
            progress_day=3,
        ),
        EventHolding(
            stadium_tel_code=StadiumTelCode.KARATSU,
            date=None,
            status=EventHoldingStatus.OPEN,
            progress_day=3,
        ),
    ]

    for expected, actual in zip(expected_results, data, strict=True):
        assert actual == expected


def test_scrape_event_holdings_with_ongoing_races() -> None:
    file_path = os.path.normpath(os.path.join(base_path, "./fixtures/2018_05_23.html"))
    with open(file_path) as file:
        data = extract_event_holdings(file)

    expected_results = [
        EventHolding(
            stadium_tel_code=StadiumTelCode.KIRYU,
            date=None,
            status=EventHoldingStatus.OPEN,
            progress_day=-1,
        ),
        EventHolding(
            stadium_tel_code=StadiumTelCode.TODA,
            date=None,
            status=EventHoldingStatus.OPEN,
            progress_day=2,
        ),
        EventHolding(
            stadium_tel_code=StadiumTelCode.GAMAGORI,
            date=None,
            status=EventHoldingStatus.OPEN,
            progress_day=5,
        ),
        EventHolding(
            stadium_tel_code=StadiumTelCode.TOKONAME,
            date=None,
            status=EventHoldingStatus.OPEN,
            progress_day=-1,
        ),
        EventHolding(
            stadium_tel_code=StadiumTelCode.MIKUNI,
            date=None,
            status=EventHoldingStatus.OPEN,
            progress_day=1,
        ),
        EventHolding(
            stadium_tel_code=StadiumTelCode.AMAGASAKI,
            date=None,
            status=EventHoldingStatus.OPEN,
            progress_day=2,
        ),
        EventHolding(
            stadium_tel_code=StadiumTelCode.NARUTO,
            date=None,
            status=EventHoldingStatus.OPEN,
            progress_day=4,
        ),
        EventHolding(
            stadium_tel_code=StadiumTelCode.MARUGAME,
            date=None,
            status=EventHoldingStatus.OPEN,
            progress_day=1,
        ),
        EventHolding(
            stadium_tel_code=StadiumTelCode.KOJIMA,
            date=None,
            status=EventHoldingStatus.OPEN,
            progress_day=-1,
        ),
        EventHolding(
            stadium_tel_code=StadiumTelCode.MIYAJIMA,
            date=None,
            status=EventHoldingStatus.OPEN,
            progress_day=3,
        ),
        EventHolding(
            stadium_tel_code=StadiumTelCode.TOKUYAMA,
            date=None,
            status=EventHoldingStatus.OPEN,
            progress_day=4,
        ),
        EventHolding(
            stadium_tel_code=StadiumTelCode.WAKAMATSU,
            date=None,
            status=EventHoldingStatus.OPEN,
            progress_day=3,
        ),
        EventHolding(
            stadium_tel_code=StadiumTelCode.FUKUOKA,
            date=None,
            status=EventHoldingStatus.OPEN,
            progress_day=2,
        ),
        EventHolding(
            stadium_tel_code=StadiumTelCode.OMURA,
            date=None,
            status=EventHoldingStatus.OPEN,
            progress_day=5,
        ),
    ]

    for expected, actual in zip(expected_results, data, strict=True):
        assert actual == expected


def test_scrape_event_holdings_excludes_next_day_presale_preview() -> None:
    """「電話投票前日発売」（翌日開催分プレビュー）にのみ登場する場を本日の
    開催状況として誤抽出しないことを保証する回帰テスト（2026-07-06 の
    bootstrap-errors アラーム原因: 戸田は本日未開催なのに前日発売欄の
    プレビュー行から OPEN として抽出されていた）。
    """
    file_path = os.path.normpath(os.path.join(base_path, "./fixtures/2026_07_06_presale_only.html"))
    with open(file_path) as file:
        data = extract_event_holdings(file)

    expected_results = [
        EventHolding(
            stadium_tel_code=StadiumTelCode.KIRYU,
            date=None,
            status=EventHoldingStatus.OPEN,
            progress_day=4,
        ),
        EventHolding(
            stadium_tel_code=StadiumTelCode.HEIWAJIMA,
            date=None,
            status=EventHoldingStatus.OPEN,
            progress_day=-1,
        ),
        EventHolding(
            stadium_tel_code=StadiumTelCode.TAMAGAWA,
            date=None,
            status=EventHoldingStatus.OPEN,
            progress_day=3,
        ),
        EventHolding(
            stadium_tel_code=StadiumTelCode.TOKONAME,
            date=None,
            status=EventHoldingStatus.OPEN,
            progress_day=1,
        ),
        EventHolding(
            stadium_tel_code=StadiumTelCode.MIKUNI,
            date=None,
            status=EventHoldingStatus.OPEN,
            progress_day=1,
        ),
        EventHolding(
            stadium_tel_code=StadiumTelCode.BIWAKO,
            date=None,
            status=EventHoldingStatus.OPEN,
            progress_day=1,
        ),
        EventHolding(
            stadium_tel_code=StadiumTelCode.SUMINOE,
            date=None,
            status=EventHoldingStatus.OPEN,
            progress_day=5,
        ),
        EventHolding(
            stadium_tel_code=StadiumTelCode.AMAGASAKI,
            date=None,
            status=EventHoldingStatus.OPEN,
            progress_day=5,
        ),
        EventHolding(
            stadium_tel_code=StadiumTelCode.TOKUYAMA,
            date=None,
            status=EventHoldingStatus.OPEN,
            progress_day=4,
        ),
        EventHolding(
            stadium_tel_code=StadiumTelCode.WAKAMATSU,
            date=None,
            status=EventHoldingStatus.OPEN,
            progress_day=1,
        ),
        EventHolding(
            stadium_tel_code=StadiumTelCode.OMURA,
            date=None,
            status=EventHoldingStatus.OPEN,
            progress_day=3,
        ),
    ]

    for expected, actual in zip(expected_results, data, strict=True):
        assert actual == expected

    assert StadiumTelCode.TODA not in [holding.stadium_tel_code for holding in data]


def test_scrape_event_holdings_with_advance_sale_races() -> None:
    file_path = os.path.normpath(os.path.join(base_path, "./fixtures/pre_sale_presents.html"))
    with open(file_path) as file:
        data = extract_event_holdings(file)

    expected_results = [
        EventHolding(
            stadium_tel_code=StadiumTelCode.KIRYU,
            date=None,
            status=EventHoldingStatus.OPEN,
            progress_day=-1,
        ),
        EventHolding(
            stadium_tel_code=StadiumTelCode.TODA,
            date=None,
            status=EventHoldingStatus.OPEN,
            progress_day=4,
        ),
        EventHolding(
            stadium_tel_code=StadiumTelCode.HAMANAKO,
            date=None,
            status=EventHoldingStatus.OPEN,
            progress_day=4,
        ),
        EventHolding(
            stadium_tel_code=StadiumTelCode.GAMAGORI,
            date=None,
            status=EventHoldingStatus.OPEN,
            progress_day=2,
        ),
        EventHolding(
            stadium_tel_code=StadiumTelCode.TOKONAME,
            date=None,
            status=EventHoldingStatus.OPEN,
            progress_day=1,
        ),
        EventHolding(
            stadium_tel_code=StadiumTelCode.MIKUNI,
            date=None,
            status=EventHoldingStatus.OPEN,
            progress_day=1,
        ),
        EventHolding(
            stadium_tel_code=StadiumTelCode.BIWAKO,
            date=None,
            status=EventHoldingStatus.OPEN,
            progress_day=-1,
        ),
        EventHolding(
            stadium_tel_code=StadiumTelCode.AMAGASAKI,
            date=None,
            status=EventHoldingStatus.OPEN,
            progress_day=4,
        ),
        EventHolding(
            stadium_tel_code=StadiumTelCode.NARUTO,
            date=None,
            status=EventHoldingStatus.OPEN,
            progress_day=-1,
        ),
        EventHolding(
            stadium_tel_code=StadiumTelCode.KOJIMA,
            date=None,
            status=EventHoldingStatus.OPEN,
            progress_day=3,
        ),
        EventHolding(
            stadium_tel_code=StadiumTelCode.MIYAJIMA,
            date=None,
            status=EventHoldingStatus.OPEN,
            progress_day=5,
        ),
        EventHolding(
            stadium_tel_code=StadiumTelCode.SHIMONOSEKI,
            date=None,
            status=EventHoldingStatus.OPEN,
            progress_day=1,
        ),
        EventHolding(
            stadium_tel_code=StadiumTelCode.WAKAMATSU,
            date=None,
            status=EventHoldingStatus.OPEN,
            progress_day=4,
        ),
        EventHolding(
            stadium_tel_code=StadiumTelCode.KARATSU,
            date=None,
            status=EventHoldingStatus.OPEN,
            progress_day=-1,
        ),
    ]

    for expected, actual in zip(expected_results, data, strict=True):
        assert actual == expected
