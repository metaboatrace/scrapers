import os

import pytest
from metaboatrace.models.race import Weather

from metaboatrace.scrapers.official.website.exceptions import DataNotReady, ScrapingError
from metaboatrace.scrapers.official.website.v1707.pages.race.common import (
    extract_weather_condition_base_data,
)

base_path = os.path.dirname(os.path.abspath(__file__))


def test_extract_weather_condition_base_data_normal():
    file_path = os.path.normpath(os.path.join(base_path, "./fixtures/weather_normal.html"))
    with open(file_path) as file:
        data = extract_weather_condition_base_data(file)

    assert data == {
        "weather": Weather.FINE,
        "wavelength": 1.0,
        "wind_angle": 315.0,
        "wind_velocity": 2.0,
        "air_temperature": 17.0,
        "water_temperature": 17.0,
    }


def test_extract_weather_condition_base_data_no_wind():
    file_path = os.path.normpath(os.path.join(base_path, "./fixtures/weather_no_wind.html"))
    with open(file_path) as file:
        data = extract_weather_condition_base_data(file)

    assert data == {
        "weather": Weather.CLOUDY,
        "wavelength": 2.0,
        "wind_angle": None,
        "wind_velocity": 0.0,
        "air_temperature": 20.5,
        "water_temperature": 18.5,
    }


def test_extract_weather_condition_base_data_empty_wavelength():
    file_path = os.path.normpath(
        os.path.join(base_path, "./fixtures/weather_empty_wavelength.html")
    )
    with open(file_path) as file:
        data = extract_weather_condition_base_data(file)

    assert data == {
        "weather": Weather.RAINY,
        "wavelength": 0.0,
        "wind_angle": 45.0,
        "wind_velocity": 5.0,
        "air_temperature": 15.5,
        "water_temperature": 16.0,
    }


def test_extract_weather_condition_base_data_various_wind_directions():
    test_cases = [
        ("is-wind1", 0.0),
        ("is-wind2", 22.5),
        ("is-wind3", 45.0),
        ("is-wind4", 67.5),
        ("is-wind5", 90.0),
        ("is-wind8", 157.5),
        ("is-wind12", 247.5),
        ("is-wind16", 337.5),
    ]

    for wind_class, expected_angle in test_cases:
        html_content = f"""<div class="weather1">
            <p class="weather1_title">水面気象情報</p>
            <div class="weather1_body is-type1__3rdadd">
                <div class="weather1_bodyUnit is-direction">
                    <p class="weather1_bodyUnitImage is-direction11 is-type1__3rdadd"></p>
                    <div class="weather1_bodyUnitLabel">
                        <span class="weather1_bodyUnitLabelTitle">気温</span>
                        <span class="weather1_bodyUnitLabelData">20.0℃</span>
                    </div>
                </div>
                <div class="weather1_bodyUnit is-weather">
                    <p class="weather1_bodyUnitImage is-weather1"></p>
                    <div class="weather1_bodyUnitLabel">
                        <span class="weather1_bodyUnitLabelTitle">晴</span>
                    </div>
                </div>
                <div class="weather1_bodyUnit is-wind">
                    <div class="weather1_bodyUnitLabel">
                        <span class="weather1_bodyUnitLabelTitle">風速</span>
                        <span class="weather1_bodyUnitLabelData">3m</span>
                    </div>
                </div>
                <div class="weather1_bodyUnit is-windDirection">
                    <p class="weather1_bodyUnitImage {wind_class}"></p>
                </div>
                <div class="weather1_bodyUnit is-waterTemperature">
                    <div class="weather1_bodyUnitLabel">
                        <span class="weather1_bodyUnitLabelTitle">水温</span>
                        <span class="weather1_bodyUnitLabelData">18.0℃</span>
                    </div>
                </div>
                <div class="weather1_bodyUnit is-wave">
                    <div class="weather1_bodyUnitLabel">
                        <span class="weather1_bodyUnitLabelTitle">波高</span>
                        <span class="weather1_bodyUnitLabelData">5cm</span>
                    </div>
                </div>
            </div>
        </div>"""

        from io import StringIO

        file = StringIO(html_content)
        data = extract_weather_condition_base_data(file)

        assert data["wind_angle"] == expected_angle, (
            f"Failed for {wind_class}: expected {expected_angle}, got {data['wind_angle']}"
        )


def test_extract_weather_condition_base_data_no_weather_container():
    html_content = "<html><body>No weather data</body></html>"
    from io import StringIO

    file = StringIO(html_content)

    # 必須要素 (.weather1) が無い場合は、従来の偶発的な AttributeError ではなく、
    # 既存のスクレイピング例外設計に揃えて ScrapingError を送出する。
    with pytest.raises(ScrapingError):
        extract_weather_condition_base_data(file)


def test_extract_weather_condition_base_data_invalid_wind_direction():
    html_content = """<div class="weather1">
        <p class="weather1_title">水面気象情報</p>
        <div class="weather1_body is-type1__3rdadd">
            <div class="weather1_bodyUnit is-direction">
                <p class="weather1_bodyUnitImage is-direction11 is-type1__3rdadd"></p>
                <div class="weather1_bodyUnitLabel">
                    <span class="weather1_bodyUnitLabelTitle">気温</span>
                    <span class="weather1_bodyUnitLabelData">20.0℃</span>
                </div>
            </div>
            <div class="weather1_bodyUnit is-weather">
                <p class="weather1_bodyUnitImage is-weather1"></p>
                <div class="weather1_bodyUnitLabel">
                    <span class="weather1_bodyUnitLabelTitle">晴</span>
                </div>
            </div>
            <div class="weather1_bodyUnit is-wind">
                <div class="weather1_bodyUnitLabel">
                    <span class="weather1_bodyUnitLabelTitle">風速</span>
                    <span class="weather1_bodyUnitLabelData">3m</span>
                </div>
            </div>
            <div class="weather1_bodyUnit is-windDirection">
                <p class="weather1_bodyUnitImage"></p>
            </div>
            <div class="weather1_bodyUnit is-waterTemperature">
                <div class="weather1_bodyUnitLabel">
                    <span class="weather1_bodyUnitLabelTitle">水温</span>
                    <span class="weather1_bodyUnitLabelData">18.0℃</span>
                </div>
            </div>
            <div class="weather1_bodyUnit is-wave">
                <div class="weather1_bodyUnitLabel">
                    <span class="weather1_bodyUnitLabelTitle">波高</span>
                    <span class="weather1_bodyUnitLabelData">5cm</span>
                </div>
            </div>
        </div>
    </div>"""

    from io import StringIO

    file = StringIO(html_content)

    # 風向きアイコンが未掲載 = 速報で天候欄が確定前の状態。DataNotReady を送出する。
    with pytest.raises(DataNotReady):
        extract_weather_condition_base_data(file)
