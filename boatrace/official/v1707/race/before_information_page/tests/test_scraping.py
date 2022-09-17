import os
from datetime import date

from boatrace.models.stadium_tel_code import StadiumTelCode
from boatrace.official.v1707.race.before_information_page.scraping import (
    CircumferenceExhibitionRecord,
    StartExhibitionRecord,
    extract_circumference_exhibition_records,
    extract_start_exhibition_records,
)

base_path = os.path.dirname(os.path.abspath(__file__))


def test_extract_start_exhibition_records():
    file_path = os.path.normpath(
        os.path.join(base_path, "./fixtures/20151116_23#_1R.html")
    )

    with open(file_path, mode="r") as file:
        data = extract_start_exhibition_records(file)

    assert data == [
        StartExhibitionRecord(
            race_holding_date=date(2015, 11, 16),
            stadium_tel_code=StadiumTelCode.KARATSU,
            race_number=1,
            pit_number=1,
            start_course=1,
            start_time=0.23,
        ),
        StartExhibitionRecord(
            race_holding_date=date(2015, 11, 16),
            stadium_tel_code=StadiumTelCode.KARATSU,
            race_number=1,
            pit_number=2,
            start_course=2,
            start_time=0.28,
        ),
        StartExhibitionRecord(
            race_holding_date=date(2015, 11, 16),
            stadium_tel_code=StadiumTelCode.KARATSU,
            race_number=1,
            pit_number=3,
            start_course=3,
            start_time=0.21,
        ),
        StartExhibitionRecord(
            race_holding_date=date(2015, 11, 16),
            stadium_tel_code=StadiumTelCode.KARATSU,
            race_number=1,
            pit_number=4,
            start_course=4,
            start_time=0.21,
        ),
        StartExhibitionRecord(
            race_holding_date=date(2015, 11, 16),
            stadium_tel_code=StadiumTelCode.KARATSU,
            race_number=1,
            pit_number=5,
            start_course=5,
            start_time=0.11,
        ),
        StartExhibitionRecord(
            race_holding_date=date(2015, 11, 16),
            stadium_tel_code=StadiumTelCode.KARATSU,
            race_number=1,
            pit_number=6,
            start_course=6,
            start_time=-0.04,
        ),
    ]


# レース欠場者とスタ展欠場者で場合分けした方がいいかと思ったがどちらも出力されるtableは同じなのでこれで網羅できたと見做す
def test_extract_start_exhibition_records_from_a_page_including_absent_racer():
    file_path = os.path.normpath(
        os.path.join(base_path, "./fixtures/20170625_06#_10R.html")
    )

    with open(file_path, mode="r") as file:
        data = extract_start_exhibition_records(file)

    assert data == [
        StartExhibitionRecord(
            race_holding_date=date(2017, 6, 25),
            stadium_tel_code=StadiumTelCode.HAMANAKO,
            race_number=10,
            pit_number=1,
            start_course=1,
            start_time=0.02,
        ),
        StartExhibitionRecord(
            race_holding_date=date(2017, 6, 25),
            stadium_tel_code=StadiumTelCode.HAMANAKO,
            race_number=10,
            pit_number=2,
            start_course=2,
            start_time=0.32,
        ),
        StartExhibitionRecord(
            race_holding_date=date(2017, 6, 25),
            stadium_tel_code=StadiumTelCode.HAMANAKO,
            race_number=10,
            pit_number=3,
            start_course=3,
            start_time=0.05,
        ),
        StartExhibitionRecord(
            race_holding_date=date(2017, 6, 25),
            stadium_tel_code=StadiumTelCode.HAMANAKO,
            race_number=10,
            pit_number=4,
            start_course=4,
            start_time=0.19,
        ),
        StartExhibitionRecord(
            race_holding_date=date(2017, 6, 25),
            stadium_tel_code=StadiumTelCode.HAMANAKO,
            race_number=10,
            pit_number=6,
            start_course=5,
            start_time=0.16,
        ),
    ]


def test_extract_circumference_exhibition_records():
    file_path = os.path.normpath(
        os.path.join(base_path, "./fixtures/20151116_23#_1R.html")
    )

    with open(file_path, mode="r") as file:
        data = extract_circumference_exhibition_records(file)

    assert data == [
        CircumferenceExhibitionRecord(
            race_holding_date=date(2015, 11, 16),
            stadium_tel_code=StadiumTelCode.KARATSU,
            race_number=1,
            pit_number=1,
            exhibition_time=6.7,
        ),
        CircumferenceExhibitionRecord(
            race_holding_date=date(2015, 11, 16),
            stadium_tel_code=StadiumTelCode.KARATSU,
            race_number=1,
            pit_number=2,
            exhibition_time=6.81,
        ),
        CircumferenceExhibitionRecord(
            race_holding_date=date(2015, 11, 16),
            stadium_tel_code=StadiumTelCode.KARATSU,
            race_number=1,
            pit_number=3,
            exhibition_time=6.84,
        ),
        CircumferenceExhibitionRecord(
            race_holding_date=date(2015, 11, 16),
            stadium_tel_code=StadiumTelCode.KARATSU,
            race_number=1,
            pit_number=4,
            exhibition_time=6.86,
        ),
        CircumferenceExhibitionRecord(
            race_holding_date=date(2015, 11, 16),
            stadium_tel_code=StadiumTelCode.KARATSU,
            race_number=1,
            pit_number=5,
            exhibition_time=6.83,
        ),
        CircumferenceExhibitionRecord(
            race_holding_date=date(2015, 11, 16),
            stadium_tel_code=StadiumTelCode.KARATSU,
            race_number=1,
            pit_number=6,
            exhibition_time=6.81,
        ),
    ]


def test_extarct_circumference_exhibition_records_including_st_absent_racer():
    file_path = os.path.normpath(
        # 5号艇がスタ展出てない
        os.path.join(
            base_path,
            "./fixtures/20170625_06#_10R.html",
        )
    )

    with open(file_path, mode="r") as file:
        data = extract_circumference_exhibition_records(file)

    assert data == [
        CircumferenceExhibitionRecord(
            race_holding_date=date(2017, 6, 25),
            stadium_tel_code=StadiumTelCode.HAMANAKO,
            race_number=10,
            pit_number=1,
            exhibition_time=6.66,
        ),
        CircumferenceExhibitionRecord(
            race_holding_date=date(2017, 6, 25),
            stadium_tel_code=StadiumTelCode.HAMANAKO,
            race_number=10,
            pit_number=2,
            exhibition_time=6.76,
        ),
        CircumferenceExhibitionRecord(
            race_holding_date=date(2017, 6, 25),
            stadium_tel_code=StadiumTelCode.HAMANAKO,
            race_number=10,
            pit_number=3,
            exhibition_time=6.71,
        ),
        CircumferenceExhibitionRecord(
            race_holding_date=date(2017, 6, 25),
            stadium_tel_code=StadiumTelCode.HAMANAKO,
            race_number=10,
            pit_number=4,
            exhibition_time=6.77,
        ),
        CircumferenceExhibitionRecord(
            race_holding_date=date(2017, 6, 25),
            stadium_tel_code=StadiumTelCode.HAMANAKO,
            race_number=10,
            pit_number=5,
            exhibition_time=6.73,
        ),
        CircumferenceExhibitionRecord(
            race_holding_date=date(2017, 6, 25),
            stadium_tel_code=StadiumTelCode.HAMANAKO,
            race_number=10,
            pit_number=6,
            exhibition_time=6.73,
        ),
    ]


def test_extract_circumference_exhibition_records_including_race_absent_racer():
    file_path = os.path.normpath(
        # 1号艇が欠場
        os.path.join(
            base_path,
            "./fixtures/20151116_03#_11R.html",
        )
    )

    with open(file_path, mode="r") as file:
        data = extract_circumference_exhibition_records(file)

    assert data == [
        CircumferenceExhibitionRecord(
            race_holding_date=date(2015, 11, 16),
            stadium_tel_code=StadiumTelCode.EDOGAWA,
            race_number=11,
            pit_number=2,
            exhibition_time=6.91,
        ),
        CircumferenceExhibitionRecord(
            race_holding_date=date(2015, 11, 16),
            stadium_tel_code=StadiumTelCode.EDOGAWA,
            race_number=11,
            pit_number=3,
            exhibition_time=7.04,
        ),
        CircumferenceExhibitionRecord(
            race_holding_date=date(2015, 11, 16),
            stadium_tel_code=StadiumTelCode.EDOGAWA,
            race_number=11,
            pit_number=4,
            exhibition_time=7,
        ),
        CircumferenceExhibitionRecord(
            race_holding_date=date(2015, 11, 16),
            stadium_tel_code=StadiumTelCode.EDOGAWA,
            race_number=11,
            pit_number=5,
            exhibition_time=7.16,
        ),
        CircumferenceExhibitionRecord(
            race_holding_date=date(2015, 11, 16),
            stadium_tel_code=StadiumTelCode.EDOGAWA,
            race_number=11,
            pit_number=6,
            exhibition_time=6.78,
        ),
    ]
