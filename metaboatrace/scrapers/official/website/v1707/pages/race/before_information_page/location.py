from datetime import date

from metaboatrace.models.stadium import StadiumTelCode

from metaboatrace.scrapers.official.website.v1707.utils import build_race_page_url


def create_race_before_information_page_url(
    race_holding_date: date, stadium_tel_code: StadiumTelCode, race_number: int
) -> str:
    return build_race_page_url("beforeinfo", race_holding_date, stadium_tel_code, race_number)
