from datetime import UTC, date, datetime

import pytest

from metaboatrace.scrapers.official.website.v1707.utils import (
    jst_wall_clock_to_utc,
    split_racer_name,
)


@pytest.mark.parametrize(
    "full_name,expected",
    [
        pytest.param("新田　芳美", ("新田", "芳美"), id="full-width space"),
        pytest.param(
            "\n 小神野紀代子\n", ("小神野紀代子", ""), id="no delimiter, surrounding whitespace"
        ),
        pytest.param("新田 芳美", ("新田", "芳美"), id="half-width space"),
        pytest.param(
            "坂口　愛　子", ("坂口", "愛　子"), id="multiple full-width delimiters split at first"
        ),
    ],
)
def test_split_racer_name(full_name: str, expected: tuple[str, str]) -> None:
    assert split_racer_name(full_name) == expected


def test_jst_wall_clock_to_utc_shifts_by_nine_hours() -> None:
    assert jst_wall_clock_to_utc(date(2026, 11, 19), 20, 41) == datetime(
        2026, 11, 19, 11, 41, tzinfo=UTC
    )


def test_jst_wall_clock_to_utc_crosses_the_utc_date_boundary() -> None:
    # JST の朝 9 時より前は UTC では前日になる (モーニングレースの 8 時台が該当)
    assert jst_wall_clock_to_utc(date(2026, 11, 19), 8, 30) == datetime(
        2026, 11, 18, 23, 30, tzinfo=UTC
    )
