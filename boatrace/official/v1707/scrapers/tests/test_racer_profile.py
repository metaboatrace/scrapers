import os
from datetime import date

import pytest
from boatrace.models.branch import Branch
from boatrace.models.prefecture import Prefecture
from boatrace.models.racer_rank import RacerRank
from boatrace.official.exceptions import DataNotFound
from boatrace.official.v1707.scrapers.racer_profile import scrape_racer_profile

base_path = os.path.dirname(os.path.abspath(__file__))


def test_scrape_a_race_information():
    file_path = os.path.normpath(
        os.path.join(base_path, "./fixtures/racer_profile/4444.html")
    )

    with open(file_path, mode="r") as file:
        data = scrape_racer_profile(file)

    assert data.__dict__ == {
        "last_name": "桐生",
        "first_name": "順平",
        "registration_number": 4444,
        "birth_date": date(1986, 10, 7),
        "height": 160,
        "weight": 53,
        "branch_prefecture": Branch.SAITAMA,
        "born_prefecture": Prefecture.FUKUSHIMA,
        "term": 100,
        "current_rating": RacerRank.A1,
    }


def test_scrape_a_no_contents_page():
    file_path = os.path.normpath(
        os.path.join(
            os.path.join(base_path, "./fixtures/racer_profile/data_not_found.html")
        )
    )

    with open(file_path, mode="r") as file:
        with pytest.raises(DataNotFound):
            scrape_racer_profile(file)
