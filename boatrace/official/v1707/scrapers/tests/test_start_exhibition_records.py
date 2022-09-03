import os
from datetime import date

from boatrace.models.stadium_tel_code import StadiumTelCode
from boatrace.official.v1707.scrapers.start_exhibition_records import (
    Dto,
    scrape_start_exhibition_records,
)

base_path = os.path.dirname(os.path.abspath(__file__))


def test_scrape_start_exhibition_records():
    file_path = os.path.normpath(
        os.path.join(
            base_path, "./fixtures/race_before_information/20151116_23#_1R.html"
        )
    )

    with open(file_path, mode="r") as file:
        data = scrape_start_exhibition_records(file)

    assert data == [
        Dto(
            race_holding_date=date(2015, 11, 16),
            stadium_tel_code=StadiumTelCode.KARATSU,
            race_number=1,
            pit_number=1,
            start_course=1,
            start_time=0.23,
        ),
        Dto(
            race_holding_date=date(2015, 11, 16),
            stadium_tel_code=StadiumTelCode.KARATSU,
            race_number=1,
            pit_number=2,
            start_course=2,
            start_time=0.28,
        ),
        Dto(
            race_holding_date=date(2015, 11, 16),
            stadium_tel_code=StadiumTelCode.KARATSU,
            race_number=1,
            pit_number=3,
            start_course=3,
            start_time=0.21,
        ),
        Dto(
            race_holding_date=date(2015, 11, 16),
            stadium_tel_code=StadiumTelCode.KARATSU,
            race_number=1,
            pit_number=4,
            start_course=4,
            start_time=0.21,
        ),
        Dto(
            race_holding_date=date(2015, 11, 16),
            stadium_tel_code=StadiumTelCode.KARATSU,
            race_number=1,
            pit_number=5,
            start_course=5,
            start_time=0.11,
        ),
        Dto(
            race_holding_date=date(2015, 11, 16),
            stadium_tel_code=StadiumTelCode.KARATSU,
            race_number=1,
            pit_number=6,
            start_course=6,
            start_time=-0.04,
        ),
    ]


# レース欠場者とスタ展欠場者で場合分けした方がいいかと思ったがどちらも出力されるtableは同じなのでこれで網羅できたと見做す
def test_scrape_start_exhibition_records_including_absent_racer():
    file_path = os.path.normpath(
        os.path.join(
            base_path, "./fixtures/race_before_information/20170625_06#_10R.html"
        )
    )

    with open(file_path, mode="r") as file:
        data = scrape_start_exhibition_records(file)

    assert data == [
        Dto(
            race_holding_date=date(2017, 6, 25),
            stadium_tel_code=StadiumTelCode.HAMANAKO,
            race_number=10,
            pit_number=1,
            start_course=1,
            start_time=0.02,
        ),
        Dto(
            race_holding_date=date(2017, 6, 25),
            stadium_tel_code=StadiumTelCode.HAMANAKO,
            race_number=10,
            pit_number=2,
            start_course=2,
            start_time=0.32,
        ),
        Dto(
            race_holding_date=date(2017, 6, 25),
            stadium_tel_code=StadiumTelCode.HAMANAKO,
            race_number=10,
            pit_number=3,
            start_course=3,
            start_time=0.05,
        ),
        Dto(
            race_holding_date=date(2017, 6, 25),
            stadium_tel_code=StadiumTelCode.HAMANAKO,
            race_number=10,
            pit_number=4,
            start_course=4,
            start_time=0.19,
        ),
        Dto(
            race_holding_date=date(2017, 6, 25),
            stadium_tel_code=StadiumTelCode.HAMANAKO,
            race_number=10,
            pit_number=6,
            start_course=5,
            start_time=0.16,
        ),
    ]
