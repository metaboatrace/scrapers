import os

import pytest
from boatrace.models.gender import Gender
from boatrace.models.racer_rank import RacerRank
from boatrace.official.exceptions import DataNotFound
from boatrace.official.v1707.scrapers.event_entries import (
    scrape_pre_inspection_information,
)

base_path = os.path.dirname(os.path.abspath(__file__))


def test_scrape_a_pre_inspection_information():
    file_path = os.path.normpath(
        os.path.join(
            base_path, "./fixtures/pre_inspection_information/20151112_23#.html"
        )
    )
    with open(file_path, mode="r") as file:
        data = scrape_pre_inspection_information(file)

    assert len(data) == 44
    assert data[0].__dict__ == {
        "racer_registration_number": 3470,
        "racer_last_name": "新田",
        "racer_first_name": "芳美",
        "racer_rank": RacerRank.A1,
        "motor_number": 70,
        "quinella_rate_of_motor": 61.6,
        "boat_number": 35,
        "quinella_rate_of_boat": 39.2,
        "anterior_time": 7.07,
        "racer_gender": Gender.FEMALE,
    }
    assert data[-1].__dict__ == {
        "racer_registration_number": 3518,
        "racer_last_name": "倉田",
        "racer_first_name": "郁美",
        "racer_rank": RacerRank.A2,
        "motor_number": 44,
        "quinella_rate_of_motor": 20.3,
        "boat_number": 36,
        "quinella_rate_of_boat": 31.7,
        "anterior_time": 6.96,
        "racer_gender": Gender.FEMALE,
    }


def test_scrape_a_no_contents_page():
    file_path = os.path.normpath(
        os.path.join(
            base_path, "./fixtures/pre_inspection_information/data_not_found.html"
        )
    )

    with open(file_path, mode="r") as file:
        with pytest.raises(DataNotFound):
            scrape_pre_inspection_information(file)


def test_scrape_a_pre_inspection_information_of_parallel_series():
    file_path = os.path.normpath(
        os.path.join(
            base_path, "./fixtures/pre_inspection_information/20191218_12#.html"
        )
    )
    with open(file_path, mode="r") as file:
        data = scrape_pre_inspection_information(file)

    assert len(data) == 59
    assert data[0].__dict__ == {
        "racer_registration_number": 4320,
        "racer_last_name": "峰",
        "racer_first_name": "竜太",
        "racer_rank": RacerRank.A1,
        "motor_number": 88,
        "quinella_rate_of_motor": 56.8,
        "boat_number": 26,
        "quinella_rate_of_boat": 45.9,
        "anterior_time": 6.7,
        "racer_gender": Gender.MALE,
    }
    assert data[-1].__dict__ == {
        "racer_registration_number": 3942,
        "racer_last_name": "寺田",
        "racer_first_name": "祥",
        "racer_rank": RacerRank.A1,
        "motor_number": 29,
        "quinella_rate_of_motor": 25.7,
        "boat_number": 87,
        "quinella_rate_of_boat": 35.6,
        "anterior_time": 6.76,
        "racer_gender": Gender.MALE,
    }
