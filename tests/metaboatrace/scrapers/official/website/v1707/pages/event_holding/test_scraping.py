import os

import pytest
from metaboatrace.models.stadium import StadiumTelCode

# from metaboatrace.scrapers.official.website.exceptions import DataNotFound, ScrapingError
from metaboatrace.scrapers.official.website.v1707.pages.event_holding_page.scraping import (
    extract_event_holdings,
)

base_path = os.path.dirname(os.path.abspath(__file__))


def test_scrape_event_holdings_with_cancellations_and_delays() -> None:
    file_path = os.path.normpath(os.path.join(base_path, "./fixtures/2015_08_25.html"))
    with open(file_path, mode="r") as file:
        data = extract_event_holdings(file)

    expected_results = [
        {"day_text": "３日目", "stadium_tel_code": StadiumTelCode.EDOGAWA},
        {"day_text": "最終日", "stadium_tel_code": StadiumTelCode.HEIWAJIMA},
        {"day_text": "初日", "stadium_tel_code": StadiumTelCode.GAMAGORI},
        {"day_text": "５日目", "stadium_tel_code": StadiumTelCode.BIWAKO},
        {"day_text": "中止順延", "stadium_tel_code": StadiumTelCode.KOJIMA},
        {"day_text": "中止順延", "stadium_tel_code": StadiumTelCode.TOKUYAMA},
        {"day_text": "中止", "stadium_tel_code": StadiumTelCode.SHIMONOSEKI},
        {"day_text": "中止順延", "stadium_tel_code": StadiumTelCode.WAKAMATSU},
        {"day_text": "中止順延", "stadium_tel_code": StadiumTelCode.FUKUOKA},
        {"day_text": "中止順延", "stadium_tel_code": StadiumTelCode.KARATSU},
        {"day_text": "中止", "stadium_tel_code": StadiumTelCode.OMURA},
    ]

    for expected, actual in zip(expected_results, data):
        assert actual == expected


def test_scrape_event_holdings_with_postponements_after_nth_race() -> None:
    file_path = os.path.normpath(os.path.join(base_path, "./fixtures/2020_08_13.html"))
    with open(file_path, mode="r") as file:
        data = extract_event_holdings(file)

    expected_results = [
        {"day_text": "初日", "stadium_tel_code": StadiumTelCode.KIRYU},
        {"day_text": "３日目", "stadium_tel_code": StadiumTelCode.TODA},
        {"day_text": "初日", "stadium_tel_code": StadiumTelCode.EDOGAWA},
        {"day_text": "初日", "stadium_tel_code": StadiumTelCode.HAMANAKO},
        {"day_text": "初日", "stadium_tel_code": StadiumTelCode.GAMAGORI},
        {"day_text": "最終日", "stadium_tel_code": StadiumTelCode.MIKUNI},
        {"day_text": "最終日", "stadium_tel_code": StadiumTelCode.BIWAKO},
        {"day_text": "中止", "stadium_tel_code": StadiumTelCode.SUMINOE},
        {"day_text": "５日目", "stadium_tel_code": StadiumTelCode.AMAGASAKI},
        {"day_text": "３日目", "stadium_tel_code": StadiumTelCode.NARUTO},
        {"day_text": "２日目", "stadium_tel_code": StadiumTelCode.MIYAJIMA},
        {"day_text": "初日", "stadium_tel_code": StadiumTelCode.TOKUYAMA},
        {"day_text": "４日目", "stadium_tel_code": StadiumTelCode.WAKAMATSU},
        {"day_text": "３日目", "stadium_tel_code": StadiumTelCode.FUKUOKA},
        {"day_text": "３日目", "stadium_tel_code": StadiumTelCode.KARATSU},
    ]

    for expected, actual in zip(expected_results, data):
        assert actual == expected


def test_scrape_event_holdings_with_ongoing_races() -> None:
    file_path = os.path.normpath(os.path.join(base_path, "./fixtures/2018_05_23.html"))
    with open(file_path, mode="r") as file:
        data = extract_event_holdings(file)

    expected_results = [
        {"day_text": "最終日", "stadium_tel_code": StadiumTelCode.KIRYU},
        {"day_text": "２日目", "stadium_tel_code": StadiumTelCode.TODA},
        {"day_text": "５日目", "stadium_tel_code": StadiumTelCode.GAMAGORI},
        {"day_text": "最終日", "stadium_tel_code": StadiumTelCode.TOKONAME},
        {"day_text": "初日", "stadium_tel_code": StadiumTelCode.MIKUNI},
        {"day_text": "２日目", "stadium_tel_code": StadiumTelCode.AMAGASAKI},
        {"day_text": "４日目", "stadium_tel_code": StadiumTelCode.NARUTO},
        {"day_text": "初日", "stadium_tel_code": StadiumTelCode.MARUGAME},
        {"day_text": "最終日", "stadium_tel_code": StadiumTelCode.KOJIMA},
        {"day_text": "３日目", "stadium_tel_code": StadiumTelCode.MIYAJIMA},
        {"day_text": "４日目", "stadium_tel_code": StadiumTelCode.TOKUYAMA},
        {"day_text": "３日目", "stadium_tel_code": StadiumTelCode.WAKAMATSU},
        {"day_text": "２日目", "stadium_tel_code": StadiumTelCode.FUKUOKA},
        {"day_text": "５日目", "stadium_tel_code": StadiumTelCode.OMURA},
    ]

    for expected, actual in zip(expected_results, data):
        assert actual == expected


def test_scrape_event_holdings_with_advance_sale_races() -> None:
    file_path = os.path.normpath(os.path.join(base_path, "./fixtures/pre_sale_presents.html"))
    with open(file_path, mode="r") as file:
        data = extract_event_holdings(file)

    expected_results = [
        {"day_text": "最終日", "stadium_tel_code": StadiumTelCode.KIRYU},
        {"day_text": "４日目", "stadium_tel_code": StadiumTelCode.TODA},
        {"day_text": "４日目", "stadium_tel_code": StadiumTelCode.HAMANAKO},
        {"day_text": "２日目", "stadium_tel_code": StadiumTelCode.GAMAGORI},
        {"day_text": "初日", "stadium_tel_code": StadiumTelCode.TOKONAME},
        {"day_text": "初日", "stadium_tel_code": StadiumTelCode.MIKUNI},
        {"day_text": "最終日", "stadium_tel_code": StadiumTelCode.BIWAKO},
        {"day_text": "４日目", "stadium_tel_code": StadiumTelCode.AMAGASAKI},
        {"day_text": "最終日", "stadium_tel_code": StadiumTelCode.NARUTO},
        {"day_text": "３日目", "stadium_tel_code": StadiumTelCode.KOJIMA},
        {"day_text": "５日目", "stadium_tel_code": StadiumTelCode.MIYAJIMA},
        {"day_text": "初日", "stadium_tel_code": StadiumTelCode.SHIMONOSEKI},
        {"day_text": "４日目", "stadium_tel_code": StadiumTelCode.WAKAMATSU},
        {"day_text": "最終日", "stadium_tel_code": StadiumTelCode.KARATSU},
    ]

    for expected, actual in zip(expected_results, data):
        assert actual == expected
