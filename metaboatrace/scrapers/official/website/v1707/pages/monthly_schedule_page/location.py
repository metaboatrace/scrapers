import urllib.parse

from metaboatrace.scrapers.official.website.v1707 import BASE_URL


def create_monthly_schedule_page_url(year: int, month: int) -> str:
    return f"{BASE_URL}/owpc/pc/race/monthlyschedule?{urllib.parse.urlencode({'year': year, 'month': month})}"
