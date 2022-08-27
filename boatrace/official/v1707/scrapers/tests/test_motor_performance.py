import os
from datetime import date

from boatrace.official.models import MotorPerformance
from boatrace.official.v1707.scrapers.motor_performance import scrape_motor_performance

base_path = os.path.dirname(os.path.abspath(__file__))


def test_scrape_motor_performance():
    file_path = os.path.normpath(
        os.path.join(base_path, "./fixtures/race_information/20180301_07#_8R.html")
    )

    with open(file_path, mode="r") as file:
        data = scrape_motor_performance(file)

    assert data == [
        MotorPerformance(
            recorded_date=date(2018, 3, 1),
            number=66,
            quinella_rate=38.1,
            trio_rate=51.9,
        ),
        MotorPerformance(
            recorded_date=date(2018, 3, 1),
            number=41,
            quinella_rate=36.5,
            trio_rate=51,
        ),
        MotorPerformance(
            recorded_date=date(2018, 3, 1),
            number=58,
            quinella_rate=33.17,
            trio_rate=51.49,
        ),
        MotorPerformance(
            recorded_date=date(2018, 3, 1),
            number=33,
            quinella_rate=39.72,
            trio_rate=55.61,
        ),
        MotorPerformance(
            recorded_date=date(2018, 3, 1),
            number=71,
            quinella_rate=29.51,
            trio_rate=46.72,
        ),
        MotorPerformance(
            recorded_date=date(2018, 3, 1),
            number=40,
            quinella_rate=33.16,
            trio_rate=49.49,
        ),
    ]


def test_scrape_motor_performance_including_missing_values():
    file_path = os.path.normpath(
        os.path.join(base_path, "./fixtures/race_information/20151116_03#_11R.html")
    )

    with open(file_path, mode="r") as file:
        data = scrape_motor_performance(file)

    assert data == [
        MotorPerformance(
            recorded_date=date(2015, 11, 16),
            number=62,
            quinella_rate=31.5,
            trio_rate=None,
        ),
        MotorPerformance(
            recorded_date=date(2015, 11, 16),
            number=61,
            quinella_rate=34.4,
            trio_rate=None,
        ),
        MotorPerformance(
            recorded_date=date(2015, 11, 16),
            number=56,
            quinella_rate=27.8,
            trio_rate=None,
        ),
        MotorPerformance(
            recorded_date=date(2015, 11, 16),
            number=68,
            quinella_rate=48.3,
            trio_rate=None,
        ),
        MotorPerformance(
            recorded_date=date(2015, 11, 16),
            number=26,
            quinella_rate=30.2,
            trio_rate=None,
        ),
        MotorPerformance(
            recorded_date=date(2015, 11, 16),
            number=20,
            quinella_rate=40.1,
            trio_rate=None,
        ),
    ]
