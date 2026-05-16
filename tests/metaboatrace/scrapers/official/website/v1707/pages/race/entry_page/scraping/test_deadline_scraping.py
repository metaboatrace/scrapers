import os
from datetime import date, datetime

import pytz

from metaboatrace.scrapers.official.website.v1707.pages.race.entry_page.scraping import (
    extract_race_deadlines,
)

base_path = os.path.dirname(os.path.abspath(__file__))
fixture_dir_path = os.path.join(base_path, os.pardir, "fixtures")

jst = pytz.timezone("Asia/Tokyo")


def test_extract_race_deadlines_from_an_entry_page() -> None:
    file_path = os.path.normpath(os.path.join(fixture_dir_path, "20151016_08#_2R.html"))
    with open(file_path, mode="r") as file:
        data = extract_race_deadlines(file)

    race_holding_date = date(2015, 10, 16)

    def deadline_at(hour: int, minute: int) -> datetime:
        return jst.localize(
            datetime(
                race_holding_date.year, race_holding_date.month, race_holding_date.day, hour, minute
            )
        ).astimezone(pytz.utc)

    assert data == {
        1: deadline_at(10, 47),
        2: deadline_at(11, 13),
        3: deadline_at(11, 39),
        4: deadline_at(12, 6),
        5: deadline_at(12, 33),
        6: deadline_at(13, 1),
        7: deadline_at(13, 29),
        8: deadline_at(13, 58),
        9: deadline_at(14, 28),
        10: deadline_at(14, 59),
        11: deadline_at(15, 30),
        12: deadline_at(16, 4),
    }


def test_extract_race_deadlines_returns_utc_aware_datetimes() -> None:
    file_path = os.path.normpath(os.path.join(fixture_dir_path, "20180301_07#_8R.html"))
    with open(file_path, mode="r") as file:
        data = extract_race_deadlines(file)

    assert len(data) == 12
    assert all(d.tzinfo == pytz.utc for d in data.values())
