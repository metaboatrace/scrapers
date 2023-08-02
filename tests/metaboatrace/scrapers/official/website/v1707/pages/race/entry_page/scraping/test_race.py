import os
from datetime import date, datetime

from metaboatrace.models.race import RaceInformation
from metaboatrace.models.stadium import StadiumTelCode

from metaboatrace.scrapers.official.website.v1707.pages.race.entry_page.scraping import (
    extract_race_information,
)

base_path = os.path.dirname(os.path.abspath(__file__))
fixture_dir_path = os.path.join(base_path, os.pardir, "fixtures")


def test_extract_race_information_from_an_entry_page() -> None:
    file_path = os.path.normpath(os.path.join(fixture_dir_path, "20151016_08#_2R.html"))
    with open(file_path, mode="r") as file:
        data = extract_race_information(file)

    assert data == RaceInformation(
        race_holding_date=date(2015, 10, 16),
        stadium_tel_code=StadiumTelCode.TOKONAME,
        race_number=2,
        title="予選",
        number_of_laps=3,
        deadline_at=datetime(2015, 10, 16, 11, 13),
        is_course_fixed=False,
        use_stabilizer=False,
    )


def test_extract_race_information_using_stabilizers_from_an_entry_page() -> None:
    file_path = os.path.normpath(os.path.join(fixture_dir_path, "20180301_07#_8R.html"))
    with open(file_path, mode="r") as file:
        data = extract_race_information(file)

    assert data == RaceInformation(
        race_holding_date=date(2018, 3, 1),
        stadium_tel_code=StadiumTelCode.GAMAGORI,
        race_number=8,
        title="一般戦",
        number_of_laps=3,
        deadline_at=datetime(2018, 3, 1, 18, 26),
        is_course_fixed=False,
        use_stabilizer=True,
    )


def test_extract_course_fixed_race_information_from_an_entry_page() -> None:
    file_path = os.path.normpath(os.path.join(fixture_dir_path, "20180301_07#_7R.html"))
    with open(file_path, mode="r") as file:
        data = extract_race_information(file)

    assert data == RaceInformation(
        race_holding_date=date(2018, 3, 1),
        stadium_tel_code=StadiumTelCode.GAMAGORI,
        race_number=7,
        title="一般戦",
        number_of_laps=3,
        deadline_at=datetime(2018, 3, 1, 17, 57),
        is_course_fixed=True,
        use_stabilizer=True,
    )


def test_extract_two_laps_race_information_from_an_entry_page() -> None:
    file_path = os.path.normpath(os.path.join(fixture_dir_path, "20180301_15#_12R.html"))
    with open(file_path, mode="r") as file:
        data = extract_race_information(file)

    assert data == RaceInformation(
        race_holding_date=date(2018, 3, 1),
        stadium_tel_code=StadiumTelCode.MARUGAME,
        race_number=12,
        title="一般選抜",
        number_of_laps=2,
        deadline_at=datetime(2018, 3, 1, 20, 42),
        is_course_fixed=False,
        use_stabilizer=True,
    )
