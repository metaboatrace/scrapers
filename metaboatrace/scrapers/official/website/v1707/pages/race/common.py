import re
from typing import IO, TypedDict

import numpy as np
from bs4 import BeautifulSoup
from metaboatrace.models.race import Weather

from metaboatrace.scrapers.official.website.exceptions import DataNotReady
from metaboatrace.scrapers.official.website.v1707.factories import WeatherFactory
from metaboatrace.scrapers.official.website.v1707.utils import select_one_or_raise


class WeatherConditionBaseData(TypedDict):
    weather: Weather
    wavelength: float
    wind_angle: float | None
    wind_velocity: float
    air_temperature: float
    water_temperature: float


def extract_weather_condition_base_data(file: IO[str]) -> WeatherConditionBaseData:
    soup = BeautifulSoup(file, "html.parser")

    WIND_ICON_IDS = list(range(1, 17))
    NO_WIND_ICON_ID = 17

    data_container = select_one_or_raise(soup, ".weather1")
    if m := re.search(
        r"is-wind(\d{1,2})",
        "".join(select_one_or_raise(data_container, ".is-windDirection p")["class"]),
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
        # 風向きアイコン未掲載 = 速報で天候欄がまだ埋まっていない (確定前)
        raise DataNotReady

    weather = WeatherFactory.create(select_one_or_raise(data_container, ".is-weather").text.strip())

    try:
        # NOTE: 数年に一度ぐらいの頻度ではあるが波高が入っていないケースがある
        # https://www.boatrace.jp/owpc/pc/race/raceresult?rno=9&jcd=23&hd=20200209
        wavelength_str = (
            data_container.select(".weather1_bodyUnitLabelData")[3].text.strip().replace("cm", "")
        )
        wavelength = float(wavelength_str) if wavelength_str else 0.0

        wind_velocity = float(
            data_container.select(".weather1_bodyUnitLabelData")[1].text.strip().replace("m", "")
        )
        air_temperature = float(
            data_container.select(".weather1_bodyUnitLabelData")[0].text.strip().replace("℃", "")
        )
        water_temperature = float(
            data_container.select(".weather1_bodyUnitLabelData")[2].text.strip().replace("℃", "")
        )
    except ValueError as e:
        # 風速・気温・水温が空 / プレースホルダ = 速報で未確定 (確定前)
        raise DataNotReady from e

    return {
        "weather": weather,
        "wavelength": wavelength,
        "wind_angle": wind_angle,
        "wind_velocity": wind_velocity,
        "air_temperature": air_temperature,
        "water_temperature": water_temperature,
    }
