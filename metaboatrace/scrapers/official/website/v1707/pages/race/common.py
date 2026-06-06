import re
from typing import IO, TypedDict

import numpy as np
from bs4 import BeautifulSoup
from metaboatrace.models.race import Weather

from metaboatrace.scrapers.official.website.exceptions import DataNotReady
from metaboatrace.scrapers.official.website.v1707.factories import WeatherFactory
from metaboatrace.scrapers.official.website.v1707.utils import select_one_or_raise

# 風向きアイコンの ID。1〜16 が各方位を表し、17 は「風向きなし」を表す。
WIND_ICON_IDS = list(range(1, 17))
NO_WIND_ICON_ID = 17


class WeatherConditionBaseData(TypedDict):
    weather: Weather
    wavelength: float
    wind_angle: float | None
    wind_velocity: float
    air_temperature: float
    water_temperature: float


def extract_weather_condition_base_data(file: IO[str]) -> WeatherConditionBaseData:
    soup = BeautifulSoup(file, "html.parser")

    data_container = select_one_or_raise(soup, ".weather1")
    if m := re.search(
        r"is-wind(\d{1,2})",
        "".join(select_one_or_raise(data_container, ".is-windDirection p")["class"]),
    ):
        wind_direction_id_in_official = int(m.group(1))
        # wind_angles は方位を角度で表した配列で、スリットの北を 0 度とする。
        # 先頭が 0 度で、以降は 22.5 度ずつ増える（0.0, 22.5, 45.0, ..., 最後は 337.5）。
        # 参考: http://boatrace.jp/static_extra/pc/images/icon_wind1_1.png
        wind_angles = np.arange(0, 361, (360 / len(WIND_ICON_IDS)))
        wind_angle = (
            None
            if wind_direction_id_in_official == NO_WIND_ICON_ID
            else wind_angles[wind_direction_id_in_official - 1]
        )

    else:
        # 風向きアイコンが未掲載なのは、速報で天候欄がまだ埋まっていない（確定前）状態
        raise DataNotReady

    weather = WeatherFactory.create(select_one_or_raise(data_container, ".is-weather").text.strip())

    try:
        # 数年に一度ぐらいの頻度だが、波高が入っていないケースがある
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
