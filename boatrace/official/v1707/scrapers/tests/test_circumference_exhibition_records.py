import os
from datetime import date

from boatrace.models.stadium_tel_code import StadiumTelCode
from boatrace.official.v1707.scrapers.circumference_exhibition_records import (
    Dto,
    scrape_circumference_exhibition_records,
)

base_path = os.path.dirname(os.path.abspath(__file__))


def test_scrape_circumference_exhibition_records():
    file_path = os.path.normpath(
        os.path.join(
            base_path, "./fixtures/race_before_information/20151116_23#_1R.html"
        )
    )

    with open(file_path, mode="r") as file:
        data = scrape_circumference_exhibition_records(file)

    assert data == [
        Dto(
            race_holding_date=date(2015, 11, 16),
            stadium_tel_code=StadiumTelCode.KARATSU,
            race_number=1,
            pit_number=1,
            exhibition_time=6.7,
        ),
        Dto(
            race_holding_date=date(2015, 11, 16),
            stadium_tel_code=StadiumTelCode.KARATSU,
            race_number=1,
            pit_number=2,
            exhibition_time=6.81,
        ),
        Dto(
            race_holding_date=date(2015, 11, 16),
            stadium_tel_code=StadiumTelCode.KARATSU,
            race_number=1,
            pit_number=3,
            exhibition_time=6.84,
        ),
        Dto(
            race_holding_date=date(2015, 11, 16),
            stadium_tel_code=StadiumTelCode.KARATSU,
            race_number=1,
            pit_number=4,
            exhibition_time=6.86,
        ),
        Dto(
            race_holding_date=date(2015, 11, 16),
            stadium_tel_code=StadiumTelCode.KARATSU,
            race_number=1,
            pit_number=5,
            exhibition_time=6.83,
        ),
        Dto(
            race_holding_date=date(2015, 11, 16),
            stadium_tel_code=StadiumTelCode.KARATSU,
            race_number=1,
            pit_number=6,
            exhibition_time=6.81,
        ),
    ]


def test_scrape_circumference_exhibition_records_including_st_absent_racer():
    file_path = os.path.normpath(
        # 5号艇がスタ展出てない
        os.path.join(
            base_path,
            "./fixtures/race_before_information/20170625_06#_10R.html",
        )
    )

    with open(file_path, mode="r") as file:
        data = scrape_circumference_exhibition_records(file)

    assert data == [
        Dto(
            race_holding_date=date(2017, 6, 25),
            stadium_tel_code=StadiumTelCode.HAMANAKO,
            race_number=10,
            pit_number=1,
            exhibition_time=6.66,
        ),
        Dto(
            race_holding_date=date(2017, 6, 25),
            stadium_tel_code=StadiumTelCode.HAMANAKO,
            race_number=10,
            pit_number=2,
            exhibition_time=6.76,
        ),
        Dto(
            race_holding_date=date(2017, 6, 25),
            stadium_tel_code=StadiumTelCode.HAMANAKO,
            race_number=10,
            pit_number=3,
            exhibition_time=6.71,
        ),
        Dto(
            race_holding_date=date(2017, 6, 25),
            stadium_tel_code=StadiumTelCode.HAMANAKO,
            race_number=10,
            pit_number=4,
            exhibition_time=6.77,
        ),
        Dto(
            race_holding_date=date(2017, 6, 25),
            stadium_tel_code=StadiumTelCode.HAMANAKO,
            race_number=10,
            pit_number=5,
            exhibition_time=6.73,
        ),
        Dto(
            race_holding_date=date(2017, 6, 25),
            stadium_tel_code=StadiumTelCode.HAMANAKO,
            race_number=10,
            pit_number=6,
            exhibition_time=6.73,
        ),
    ]


def test_scrape_circumference_exhibition_records_including_race_absent_racer():
    file_path = os.path.normpath(
        # 1号艇が欠場
        os.path.join(
            base_path,
            "./fixtures/race_before_information/20151116_03#_11R.html",
        )
    )

    with open(file_path, mode="r") as file:
        data = scrape_circumference_exhibition_records(file)

    assert data == [
        Dto(
            race_holding_date=date(2015, 11, 16),
            stadium_tel_code=StadiumTelCode.EDOGAWA,
            race_number=11,
            pit_number=2,
            exhibition_time=6.91,
        ),
        Dto(
            race_holding_date=date(2015, 11, 16),
            stadium_tel_code=StadiumTelCode.EDOGAWA,
            race_number=11,
            pit_number=3,
            exhibition_time=7.04,
        ),
        Dto(
            race_holding_date=date(2015, 11, 16),
            stadium_tel_code=StadiumTelCode.EDOGAWA,
            race_number=11,
            pit_number=4,
            exhibition_time=7,
        ),
        Dto(
            race_holding_date=date(2015, 11, 16),
            stadium_tel_code=StadiumTelCode.EDOGAWA,
            race_number=11,
            pit_number=5,
            exhibition_time=7.16,
        ),
        Dto(
            race_holding_date=date(2015, 11, 16),
            stadium_tel_code=StadiumTelCode.EDOGAWA,
            race_number=11,
            pit_number=6,
            exhibition_time=6.78,
        ),
    ]
