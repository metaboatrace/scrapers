import os
from datetime import date

import pytest
from boatrace.models import BettingMethod, StadiumTelCode
from boatrace.official.exceptions import DataNotFound, RaceCanceled
from boatrace.official.v1707.race.result_page.scraping import (
    Payoff,
    extract_race_payoffs,
)

base_path = os.path.dirname(os.path.abspath(__file__))


def test_extract_race_payoffs():
    file_path = os.path.normpath(
        os.path.join(base_path, "./fixtures/20151115_07#_12R.html")
    )
    with open(file_path, mode="r") as file:
        data = extract_race_payoffs(file)

    assert data == [
        Payoff(
            race_holding_date=date(2015, 11, 15),
            stadium_tel_code=StadiumTelCode.GAMAGORI,
            race_number=12,
            betting_method=BettingMethod.TRIFECTA,
            betting_number=435,
            amount=56670,
        )
    ]


def test_extract_payoffs_from_a_race_which_has_an_absent():
    file_path = os.path.normpath(
        os.path.join(base_path, "./fixtures/20151116_03#_11R.html")
    )
    with open(file_path, mode="r") as file:
        data = extract_race_payoffs(file)

    assert data == [
        Payoff(
            race_holding_date=date(2015, 11, 16),
            stadium_tel_code=StadiumTelCode.EDOGAWA,
            race_number=11,
            betting_method=BettingMethod.TRIFECTA,
            betting_number=234,
            amount=3100,
        )
    ]


def test_extract_payoffs_from_a_race_which_has_a_tie():
    file_path = os.path.normpath(
        os.path.join(base_path, "./fixtures/20181116_18#_7R.html")
    )

    with open(file_path, mode="r") as file:
        data = extract_race_payoffs(file)

    assert data == [
        Payoff(
            race_holding_date=date(2018, 11, 16),
            stadium_tel_code=StadiumTelCode.TOKUYAMA,
            race_number=7,
            betting_method=BettingMethod.TRIFECTA,
            betting_number=142,
            amount=2230,
        ),
        Payoff(
            race_holding_date=date(2018, 11, 16),
            stadium_tel_code=StadiumTelCode.TOKUYAMA,
            race_number=7,
            betting_method=BettingMethod.TRIFECTA,
            betting_number=412,
            amount=15500,
        ),
    ]


def test_extract_payoffs_from_a_race_which_has_four_disqualified_racers():
    file_path = os.path.normpath(
        os.path.join(base_path, "./fixtures/20151114_02#_2R.html")
    )
    with open(file_path, mode="r") as file:
        data = extract_race_payoffs(file)

    assert data == []


def test_extract_payoffs_from_a_no_contents_page():
    file_path = os.path.normpath(
        os.path.join(base_path, "./fixtures/data_not_found.html")
    )

    with open(file_path, mode="r") as file:
        with pytest.raises(DataNotFound):
            extract_race_payoffs(file)


def test_extract_payoffs_from_a_canceled_race():
    file_path = os.path.normpath(os.path.join(base_path, "./fixtures/canceled.html"))

    with open(file_path, mode="r") as file:
        with pytest.raises(RaceCanceled):
            extract_race_payoffs(file)
