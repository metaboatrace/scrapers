import os
from datetime import date

import pytest
from boatrace.models.betting_method import BettingMethod
from boatrace.models.stadium_tel_code import StadiumTelCode
from boatrace.official.exceptions import DataNotFound, RaceCanceled
from boatrace.official.v1707.scrapers.race_payoff import scrape_race_payoff

base_path = os.path.dirname(os.path.abspath(__file__))


def test_scrape_a_race():
    file_path = os.path.normpath(
        os.path.join(base_path, "./fixtures/race_result/20151115_07#_12R.html")
    )
    with open(file_path, mode="r") as file:
        data = scrape_race_payoff(file)

    assert len(data) == 1
    assert data[0].__dict__ == {
        "race_holding_date": date(2015, 11, 15),
        "stadium_tel_code": StadiumTelCode.GAMAGORI,
        "race_number": 12,
        "betting_method": BettingMethod.TRIFECTA,
        "betting_number": 435,
        "amount": 56670,
    }


def test_scrape_a_race_which_has_an_absent():
    file_path = os.path.normpath(
        os.path.join(base_path, "./fixtures/race_result/20151116_03#_11R.html")
    )
    with open(file_path, mode="r") as file:
        data = scrape_race_payoff(file)

    assert data[0].__dict__ == {
        "race_holding_date": date(2015, 11, 16),
        "stadium_tel_code": StadiumTelCode.EDOGAWA,
        "race_number": 11,
        "betting_method": BettingMethod.TRIFECTA,
        "betting_number": 234,
        "amount": 3100,
    }


def test_scrape_a_race_which_has_four_disqualified_racers():
    file_path = os.path.normpath(
        os.path.join(base_path, "./fixtures/race_result/20151114_02#_2R.html")
    )
    with open(file_path, mode="r") as file:
        data = scrape_race_payoff(file)

    assert data == []


def test_scrape_a_no_contents_page():
    file_path = os.path.normpath(
        os.path.join(base_path, "./fixtures/race_result/data_not_found.html")
    )

    with open(file_path, mode="r") as file:
        with pytest.raises(DataNotFound):
            scrape_race_payoff(file)


def test_scrape_a_canceled_race():
    file_path = os.path.normpath(
        os.path.join(base_path, "./fixtures/race_result/canceled.html")
    )

    with open(file_path, mode="r") as file:
        with pytest.raises(RaceCanceled):
            scrape_race_payoff(file)
