import os
from datetime import date

import pytest
from boatrace.models.disqualification import Disqualification
from boatrace.models.stadium_tel_code import StadiumTelCode
from boatrace.models.winning_trick import WinningTrick
from boatrace.official.exceptions import DataNotFound, RaceCanceled
from boatrace.official.v1707.scrapers.race_records import Dto, scrape_race_records

base_path = os.path.dirname(os.path.abspath(__file__))


def test_scrape_a_race_includes_lateness_entry():
    file_path = os.path.normpath(
        os.path.join(base_path, "./fixtures/race_result/20151116_09#_7R.html")
    )

    with open(file_path, mode="r") as file:
        data = scrape_race_records(file)

    assert data == [
        Dto(
            race_holding_date=date(2015, 11, 16),
            stadium_tel_code=StadiumTelCode.TSU,
            race_number=7,
            pit_number=1,
            start_course=1,
            arrival=2,
            total_time=110.9,
            start_time=0.06,
            winning_trick=None,
            disqualification=None,
        ),
        Dto(
            race_holding_date=date(2015, 11, 16),
            stadium_tel_code=StadiumTelCode.TSU,
            race_number=7,
            pit_number=2,
            start_course=None,
            arrival=None,
            total_time=None,
            start_time=None,
            winning_trick=None,
            disqualification=Disqualification.LATENESS,
        ),
        Dto(
            race_holding_date=date(2015, 11, 16),
            stadium_tel_code=StadiumTelCode.TSU,
            race_number=7,
            pit_number=3,
            start_course=3,
            arrival=3,
            total_time=112.5,
            start_time=0.22,
            winning_trick=None,
            disqualification=None,
        ),
        Dto(
            race_holding_date=date(2015, 11, 16),
            stadium_tel_code=StadiumTelCode.TSU,
            race_number=7,
            pit_number=4,
            start_course=4,
            arrival=1,
            total_time=109.9,
            start_time=0.21,
            winning_trick=WinningTrick.SASHI,
            disqualification=None,
        ),
        Dto(
            race_holding_date=date(2015, 11, 16),
            stadium_tel_code=StadiumTelCode.TSU,
            race_number=7,
            pit_number=5,
            start_course=5,
            arrival=4,
            total_time=113.5,
            start_time=0.23,
            winning_trick=None,
            disqualification=None,
        ),
        Dto(
            race_holding_date=date(2015, 11, 16),
            stadium_tel_code=StadiumTelCode.TSU,
            race_number=7,
            pit_number=6,
            start_course=2,
            arrival=5,
            total_time=None,
            start_time=0.1,
            winning_trick=None,
            disqualification=None,
        ),
    ]


def test_scrape_a_race_which_has_a_tie():
    file_path = os.path.normpath(
        os.path.join(base_path, "./fixtures/race_result/20181116_18#_7R.html")
    )

    with open(file_path, mode="r") as file:
        data = scrape_race_records(file)

    assert data == [
        Dto(
            race_holding_date=date(2018, 11, 16),
            stadium_tel_code=StadiumTelCode.TOKUYAMA,
            race_number=7,
            pit_number=1,
            start_course=1,
            arrival=1,
            total_time=111.4,
            start_time=0.1,
            winning_trick=WinningTrick.NUKI,
            disqualification=None,
        ),
        Dto(
            race_holding_date=date(2018, 11, 16),
            stadium_tel_code=StadiumTelCode.TOKUYAMA,
            race_number=7,
            pit_number=2,
            start_course=2,
            arrival=3,
            total_time=114.3,
            start_time=0.16,
            winning_trick=None,
            disqualification=None,
        ),
        Dto(
            race_holding_date=date(2018, 11, 16),
            stadium_tel_code=StadiumTelCode.TOKUYAMA,
            race_number=7,
            pit_number=3,
            start_course=3,
            arrival=4,
            total_time=114.6,
            start_time=0.15,
            winning_trick=None,
            disqualification=None,
        ),
        Dto(
            race_holding_date=date(2018, 11, 16),
            stadium_tel_code=StadiumTelCode.TOKUYAMA,
            race_number=7,
            pit_number=4,
            start_course=4,
            arrival=1,
            total_time=111.4,
            start_time=0.17,
            winning_trick=WinningTrick.NUKI,
            disqualification=None,
        ),
        Dto(
            race_holding_date=date(2018, 11, 16),
            stadium_tel_code=StadiumTelCode.TOKUYAMA,
            race_number=7,
            pit_number=5,
            start_course=5,
            arrival=6,
            total_time=None,
            start_time=0.19,
            winning_trick=None,
            disqualification=None,
        ),
        Dto(
            race_holding_date=date(2018, 11, 16),
            stadium_tel_code=StadiumTelCode.TOKUYAMA,
            race_number=7,
            pit_number=6,
            start_course=6,
            arrival=5,
            total_time=None,
            start_time=0.19,
            winning_trick=None,
            disqualification=None,
        ),
    ]


def test_scrape_a_race_which_has_four_disqualified_racers():
    file_path = os.path.normpath(
        os.path.join(base_path, "./fixtures/race_result/20151114_02#_2R.html")
    )
    with open(file_path, mode="r") as file:
        data = scrape_race_records(file)

    assert [
        Dto(
            race_holding_date=date(2015, 11, 14),
            stadium_tel_code=StadiumTelCode.TODA,
            race_number=2,
            pit_number=1,
            start_course=1,
            arrival=2,
            total_time=112.7,
            start_time=0.35,
            winning_trick=None,
            disqualification=None,
        ),
        Dto(
            race_holding_date=date(2015, 11, 14),
            stadium_tel_code=StadiumTelCode.TODA,
            race_number=2,
            pit_number=2,
            start_course=2,
            arrival=1,
            total_time=111.8,
            start_time=0.11,
            winning_trick=WinningTrick.MEGUMARE,
            disqualification=None,
        ),
        Dto(
            race_holding_date=date(2015, 11, 14),
            stadium_tel_code=StadiumTelCode.TODA,
            race_number=2,
            pit_number=3,
            start_course=3,
            arrival=None,
            total_time=None,
            start_time=-0.01,
            winning_trick=None,
            disqualification=Disqualification.FLYING,
        ),
        Dto(
            race_holding_date=date(2015, 11, 14),
            stadium_tel_code=StadiumTelCode.TODA,
            race_number=2,
            pit_number=4,
            start_course=4,
            arrival=None,
            total_time=None,
            start_time=-0.01,
            winning_trick=None,
            disqualification=Disqualification.FLYING,
        ),
        Dto(
            race_holding_date=date(2015, 11, 14),
            stadium_tel_code=StadiumTelCode.TODA,
            race_number=2,
            pit_number=5,
            start_course=5,
            arrival=None,
            total_time=None,
            start_time=-0.01,
            winning_trick=None,
            disqualification=Disqualification.FLYING,
        ),
        Dto(
            race_holding_date=date(2015, 11, 14),
            stadium_tel_code=StadiumTelCode.TODA,
            race_number=2,
            pit_number=6,
            start_course=6,
            arrival=None,
            total_time=None,
            start_time=-0.01,
            winning_trick=None,
            disqualification=Disqualification.FLYING,
        ),
    ]


def test_scrape_a_no_contents_page():
    file_path = os.path.normpath(
        os.path.join(base_path, "./fixtures/race_result/data_not_found.html")
    )

    with open(file_path, mode="r") as file:
        with pytest.raises(DataNotFound):
            scrape_race_records(file)


def test_scrape_a_canceled_race():
    file_path = os.path.normpath(
        os.path.join(base_path, "./fixtures/race_result/canceled.html")
    )

    with open(file_path, mode="r") as file:
        with pytest.raises(RaceCanceled):
            scrape_race_records(file)
