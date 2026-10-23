import pytest

from metaboatrace.scrapers.official.website.v1707.utils import split_racer_name


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
