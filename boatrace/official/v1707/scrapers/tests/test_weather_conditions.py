import os
from datetime import date

import pytest
from boatrace.models.stadium_tel_code import StadiumTelCode
from boatrace.models.weather import Weather
from boatrace.official.v1707.scrapers.weather_conditions import (
    Dto,
    scrape_weather_condition,
)

base_path = os.path.dirname(os.path.abspath(__file__))


def test_scrape_weather_condition_from_a_race_before_information():
    file_path = os.path.normpath(
        os.path.join(
            base_path, "./fixtures/race_before_information/20151115_07#_12R.html"
        )
    )

    with open(file_path, mode="r") as file:
        data = scrape_weather_condition(file)

    assert data == Dto(
        race_holding_date=date(2015, 11, 15),
        stadium_tel_code=StadiumTelCode.GAMAGORI,
        race_number=12,
        in_performance=False,
        weather=Weather.FINE,
        wavelength=2.0,
        wind_angle=315.0,
        wind_velocity=4.0,
        air_temperature=17.0,
        water_temperature=17.0,
    )


def test_scrape_weather_condition_from_a_race_result():
    file_path = os.path.normpath(
        os.path.join(base_path, "./fixtures/race_result/20181116_18#_7R.html")
    )

    with open(file_path, mode="r") as file:
        data = scrape_weather_condition(file)

    assert data == Dto(
        race_holding_date=date(2018, 11, 16),
        stadium_tel_code=StadiumTelCode.TOKUYAMA,
        race_number=7,
        in_performance=True,
        weather=Weather.CLOUDY,
        wavelength=1.0,
        wind_angle=135.0,
        wind_velocity=1.0,
        air_temperature=15.0,
        water_temperature=18.0,
    )


def test_scrape_weather_condition_of_extreme_weather():
    file_path = os.path.normpath(
        os.path.join(
            base_path, "./fixtures/race_before_information/20171022_07#_1R.html"
        )
    )

    with open(file_path, mode="r") as file:
        with pytest.raises(ValueError):
            # 風向きのデータが入らないから、HTMLクラスのパターンなどがマッチしなくてこの例外になる
            scrape_weather_condition(file)


def test_scrape_incomplete_information():
    file_path = os.path.normpath(
        os.path.join(
            base_path, "./fixtures/race_before_information/20171030_03#_1R.html"
        )
    )

    with open(file_path, mode="r") as file:
        data = scrape_weather_condition(file)

    import pdb

    pdb.set_trace()

    with open(file_path, mode="r") as file:
        with pytest.raises(ValueError):
            # 風向きのデータが入らないから、HTMLクラスのパターンなどがマッチしなくてこの例外になる
            scrape_weather_condition(file)


def test_scrape_incomplete_information():
    file_path = os.path.normpath(
        os.path.join(
            base_path, "./fixtures/race_before_information/20171030_03#_1R.html"
        )
    )

    with open(file_path, mode="r") as file:
        with pytest.raises(ValueError):
            # 0:00現在表示があったら欠損値があるはずなのでこの例外になる
            scrape_weather_condition(file)
