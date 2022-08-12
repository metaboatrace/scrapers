import os
from datetime import date, datetime

from boatrace.models.race_laps import RaceLaps
from boatrace.models.stadium_tel_code import StadiumTelCode
from boatrace.official.v1707.scrapers.race_information import scrape_race_information

base_path = os.path.dirname(os.path.abspath(__file__))


def test_scrape_a_race_information():
    file_path = os.path.normpath(
        os.path.join(base_path, "./fixtures/race_information/20151016_08#_2R.html")
    )
    with open(file_path, mode="r") as file:
        data = scrape_race_information(file)

    assert data.__dict__ == {
        "date": date(2015, 10, 16),
        "stadium_tel_code": StadiumTelCode.TOKONAME,
        "number": 2,
        "title": "予選",
        "race_laps": RaceLaps.THREE,
        "deadline_at": datetime(2015, 10, 16, 11, 13),
        "is_course_fixed": False,
        "use_stabilizer": False,
    }


def test_scrape_a_race_information_which_uses_stabilizers():
    file_path = os.path.normpath(
        os.path.join(base_path, "./fixtures/race_information/20180301_07#_8R.html")
    )
    with open(file_path, mode="r") as file:
        data = scrape_race_information(file)

    assert data.__dict__ == {
        "date": date(2018, 3, 1),
        "stadium_tel_code": StadiumTelCode.GAMAGORI,
        "number": 8,
        "title": "一般戦",
        "race_laps": RaceLaps.THREE,
        "deadline_at": datetime(2018, 3, 1, 18, 26),
        "is_course_fixed": False,
        "use_stabilizer": True,
    }


def test_scrape_a_race_information_which_is_course_fixed():
    file_path = os.path.normpath(
        os.path.join(base_path, "./fixtures/race_information/20180301_07#_7R.html")
    )
    with open(file_path, mode="r") as file:
        data = scrape_race_information(file)

    assert data.__dict__ == {
        "date": date(2018, 3, 1),
        "stadium_tel_code": StadiumTelCode.GAMAGORI,
        "number": 7,
        "title": "一般戦",
        "race_laps": RaceLaps.THREE,
        "deadline_at": datetime(2018, 3, 1, 17, 57),
        "is_course_fixed": True,
        "use_stabilizer": True,
    }


def test_scrape_a_race_information_which_is_who_laps():
    file_path = os.path.normpath(
        os.path.join(base_path, "./fixtures/race_information/20180301_15#_12R.html")
    )
    with open(file_path, mode="r") as file:
        data = scrape_race_information(file)

    assert data.__dict__ == {
        "date": date(2018, 3, 1),
        "stadium_tel_code": StadiumTelCode.MARUGAME,
        "number": 12,
        "title": "一般選抜",
        "race_laps": RaceLaps.TWO,
        "deadline_at": datetime(2018, 3, 1, 20, 42),
        "is_course_fixed": False,
        "use_stabilizer": True,
    }
