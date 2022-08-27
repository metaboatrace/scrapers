import os
from datetime import date

from boatrace.official.models import BoatPerformance
from boatrace.official.v1707.scrapers.boat_performance import scrape_boat_performance

base_path = os.path.dirname(os.path.abspath(__file__))


def test_scrape_boat_performance():
    file_path = os.path.normpath(
        os.path.join(base_path, "./fixtures/race_information/20180301_07#_8R.html")
    )

    with open(file_path, mode="r") as file:
        data = scrape_boat_performance(file)

    assert data == [
        BoatPerformance(
            recorded_date=date(2018, 3, 1),
            number=40,
            quinella_rate=39.18,
            trio_rate=57.22,
        ),
        BoatPerformance(
            recorded_date=date(2018, 3, 1),
            number=43,
            quinella_rate=37.65,
            trio_rate=55.29,
        ),
        BoatPerformance(
            recorded_date=date(2018, 3, 1),
            number=74,
            quinella_rate=35.62,
            trio_rate=54.79,
        ),
        BoatPerformance(
            recorded_date=date(2018, 3, 1),
            number=13,
            quinella_rate=29.78,
            trio_rate=45.51,
        ),
        BoatPerformance(
            recorded_date=date(2018, 3, 1),
            number=65,
            quinella_rate=27.43,
            trio_rate=50.86,
        ),
        BoatPerformance(
            recorded_date=date(2018, 3, 1),
            number=68,
            quinella_rate=28.49,
            trio_rate=45.35,
        ),
    ]


def test_scrape_boat_performance_including_missing_values():
    file_path = os.path.normpath(
        os.path.join(base_path, "./fixtures/race_information/20151116_03#_11R.html")
    )

    with open(file_path, mode="r") as file:
        data = scrape_boat_performance(file)

    assert data == [
        BoatPerformance(
            recorded_date=date(2015, 11, 16),
            number=25,
            quinella_rate=30.3,
            trio_rate=None,
        ),
        BoatPerformance(
            recorded_date=date(2015, 11, 16),
            number=31,
            quinella_rate=31.9,
            trio_rate=None,
        ),
        BoatPerformance(
            recorded_date=date(2015, 11, 16),
            number=60,
            quinella_rate=30.4,
            trio_rate=None,
        ),
        BoatPerformance(
            recorded_date=date(2015, 11, 16),
            number=43,
            quinella_rate=33.5,
            trio_rate=None,
        ),
        BoatPerformance(
            recorded_date=date(2015, 11, 16),
            number=46,
            quinella_rate=31.3,
            trio_rate=None,
        ),
        BoatPerformance(
            recorded_date=date(2015, 11, 16),
            number=69,
            quinella_rate=29,
            trio_rate=None,
        ),
    ]
