from pathlib import Path

from metaboatrace.scrapers.official.website.v1707.pages.race.entry_page.scraping import (
    is_deadline_changed,
)

FIXTURE_DIR = Path(__file__).parent.parent / "fixtures"


def test_scraping_in_not_deadline_changed_page() -> None:
    file_path = FIXTURE_DIR / "20180301_07#_8R.html"

    with open(file_path) as file:
        assert not is_deadline_changed(file)


def test_scraping_in_deadline_changed_page() -> None:
    file_path = FIXTURE_DIR / "20240104_14#_8R.html"

    with open(file_path) as file:
        assert is_deadline_changed(file)
