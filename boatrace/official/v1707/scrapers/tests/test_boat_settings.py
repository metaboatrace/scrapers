import os
from datetime import date

import pytest
from boatrace.models.stadium_tel_code import StadiumTelCode
from boatrace.official.exceptions import DataNotFound
from boatrace.official.v1707.scrapers.boat_settings import Dto, scrape_boat_settings

base_path = os.path.dirname(os.path.abspath(__file__))


def test_scrape_boat_settings():
    file_path = os.path.normpath(
        os.path.join(
            base_path, "./fixtures/race_before_information/20151116_23#_1R.html"
        )
    )

    with open(file_path, mode="r") as file:
        data = scrape_boat_settings(file)

    assert data == [
        Dto(
            race_holding_date=date(2015, 11, 16),
            stadium_tel_code=StadiumTelCode.KARATSU,
            race_number=1,
            pit_number=1,
            tilt=-0.5,
            is_new_propeller=False,
        ),
        Dto(
            race_holding_date=date(2015, 11, 16),
            stadium_tel_code=StadiumTelCode.KARATSU,
            race_number=1,
            pit_number=2,
            tilt=-0.5,
            is_new_propeller=False,
        ),
        Dto(
            race_holding_date=date(2015, 11, 16),
            stadium_tel_code=StadiumTelCode.KARATSU,
            race_number=1,
            pit_number=3,
            tilt=-0.5,
            is_new_propeller=False,
        ),
        Dto(
            race_holding_date=date(2015, 11, 16),
            stadium_tel_code=StadiumTelCode.KARATSU,
            race_number=1,
            pit_number=4,
            tilt=-0.5,
            is_new_propeller=False,
        ),
        Dto(
            race_holding_date=date(2015, 11, 16),
            stadium_tel_code=StadiumTelCode.KARATSU,
            race_number=1,
            pit_number=5,
            tilt=-0.5,
            is_new_propeller=False,
        ),
        Dto(
            race_holding_date=date(2015, 11, 16),
            stadium_tel_code=StadiumTelCode.KARATSU,
            race_number=1,
            pit_number=6,
            tilt=-0.5,
            is_new_propeller=False,
        ),
    ]


def test_scrape_boat_settings_including_propeller_exchanges():
    file_path = os.path.normpath(
        os.path.join(
            base_path, "./fixtures/race_before_information/20180619_04#_4R.html"
        )
    )

    with open(file_path, mode="r") as file:
        data = scrape_boat_settings(file)

    assert data == [
        Dto(
            race_holding_date=date(2018, 6, 19),
            stadium_tel_code=StadiumTelCode.HEIWAJIMA,
            race_number=4,
            pit_number=1,
            tilt=-0.5,
            is_new_propeller=False,
        ),
        Dto(
            race_holding_date=date(2018, 6, 19),
            stadium_tel_code=StadiumTelCode.HEIWAJIMA,
            race_number=4,
            pit_number=2,
            tilt=-0.5,
            is_new_propeller=False,
        ),
        Dto(
            race_holding_date=date(2018, 6, 19),
            stadium_tel_code=StadiumTelCode.HEIWAJIMA,
            race_number=4,
            pit_number=3,
            tilt=-0.5,
            is_new_propeller=False,
        ),
        Dto(
            race_holding_date=date(2018, 6, 19),
            stadium_tel_code=StadiumTelCode.HEIWAJIMA,
            race_number=4,
            pit_number=4,
            tilt=-0.5,
            is_new_propeller=True,
        ),
        Dto(
            race_holding_date=date(2018, 6, 19),
            stadium_tel_code=StadiumTelCode.HEIWAJIMA,
            race_number=4,
            pit_number=5,
            tilt=-0.5,
            is_new_propeller=False,
        ),
        Dto(
            race_holding_date=date(2018, 6, 19),
            stadium_tel_code=StadiumTelCode.HEIWAJIMA,
            race_number=4,
            pit_number=6,
            tilt=-0.5,
            is_new_propeller=False,
        ),
    ]


def test_scrape_boat_settings_including_absent_racers():
    file_path = os.path.normpath(
        os.path.join(
            base_path, "./fixtures/race_before_information/20151116_03#_11R.html"
        )
    )

    with open(file_path, mode="r") as file:
        data = scrape_boat_settings(file)

    assert data == [
        Dto(
            race_holding_date=date(2015, 11, 16),
            stadium_tel_code=StadiumTelCode.EDOGAWA,
            race_number=11,
            pit_number=2,
            tilt=0,
            is_new_propeller=False,
        ),
        Dto(
            race_holding_date=date(2015, 11, 16),
            stadium_tel_code=StadiumTelCode.EDOGAWA,
            race_number=11,
            pit_number=3,
            tilt=0,
            is_new_propeller=False,
        ),
        Dto(
            race_holding_date=date(2015, 11, 16),
            stadium_tel_code=StadiumTelCode.EDOGAWA,
            race_number=11,
            pit_number=4,
            tilt=0,
            is_new_propeller=False,
        ),
        Dto(
            race_holding_date=date(2015, 11, 16),
            stadium_tel_code=StadiumTelCode.EDOGAWA,
            race_number=11,
            pit_number=5,
            tilt=0,
            is_new_propeller=False,
        ),
        Dto(
            race_holding_date=date(2015, 11, 16),
            stadium_tel_code=StadiumTelCode.EDOGAWA,
            race_number=11,
            pit_number=6,
            tilt=0.5,
            is_new_propeller=False,
        ),
    ]


def test_scrape_boat_settings():
    file_path = os.path.normpath(
        os.path.join(
            base_path, "./fixtures/race_before_information/20200630_12#_12R.html"
        )
    )

    with open(file_path, mode="r") as file:
        with pytest.raises(DataNotFound):
            scrape_boat_settings(file)
