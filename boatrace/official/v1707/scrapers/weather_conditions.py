import re
from dataclasses import dataclass
from datetime import date
from typing import IO

import numpy as np
from boatrace.models.stadium_tel_code import StadiumTelCode
from boatrace.models.weather import Weather, WeatherFactory
from boatrace.official.v1707.scrapers.decorators import (
    no_content_handleable,
    race_cancellation_handleable,
)
from boatrace.official.v1707.scrapers.utils import parse_race_key_attributes
from bs4 import BeautifulSoup


@dataclass(frozen=True)
class Dto:
    race_holding_date: date
    stadium_tel_code: StadiumTelCode
    race_number: int
    in_performance: bool
    weather: Weather
    wavelength: float
    wind_angle: float
    wind_velocity: float
    air_temperature: float
    water_temperature: float


@no_content_handleable
@race_cancellation_handleable
def scrape_weather_condition(file: IO) -> Dto:
    soup = BeautifulSoup(file, "html.parser")
    race_key_attributes = parse_race_key_attributes(soup)

    active_tab = soup.select_one(
        "body > main > div > div > div > div.contentsFrame1_inner > div.tab3.is-type1__3rdadd > ul > li.is-active"
    )
    if active_tab.text == "直前情報":
        in_performance = False
    elif active_tab.text == "結果":
        in_performance = True
    else:
        raise ValueError

    WIND_ICON_IDS = list(range(1, 17))
    NO_WIND_ICON_ID = 17

    data_container = soup.select_one(".weather1")
    if m := re.search(
        r"is-wind(\d{1,2})",
        "".join(data_container.select_one(".is-windDirection p")["class"]),
    ):
        wind_direction_id_in_official = int(m.group(1))
        # NOTE: 方位を角度としてとった風向きの配列。スリットの北が0度。
        # http://boatrace.jp/static_extra/pc/images/icon_wind1_1.png
        #
        # 先頭の要素は0°で、以降22.5°ずつ増えていく
        # wind_clock_angles[0]
        # => 0.0
        # wind_clock_angles[1]
        # => 22.5
        # wind_clock_angles[2]
        # => 90.0
        # wind_clock_angles[15]
        # => 337.5
        wind_angles = np.arange(0, 361, (360 / len(WIND_ICON_IDS)))
        wind_angle = (
            None
            if wind_direction_id_in_official == NO_WIND_ICON_ID
            else wind_angles[wind_direction_id_in_official - 1]
        )

    else:
        raise ValueError

    weather = WeatherFactory.create(
        data_container.select_one(".is-weather").text.strip()
    )
    wavelength = float(
        data_container.select(".weather1_bodyUnitLabelData")[3]
        .text.strip()
        .replace("cm", "")
    )
    wind_velocity = float(
        data_container.select(".weather1_bodyUnitLabelData")[1]
        .text.strip()
        .replace("m", "")
    )
    air_temperature = float(
        data_container.select(".weather1_bodyUnitLabelData")[0]
        .text.strip()
        .replace("℃", "")
    )
    water_temperature = float(
        data_container.select(".weather1_bodyUnitLabelData")[2]
        .text.strip()
        .replace("℃", "")
    )

    return Dto(
        **race_key_attributes,
        in_performance=in_performance,
        weather=weather,
        wavelength=wavelength,
        wind_angle=wind_angle,
        wind_velocity=wind_velocity,
        air_temperature=air_temperature,
        water_temperature=water_temperature,
    )
