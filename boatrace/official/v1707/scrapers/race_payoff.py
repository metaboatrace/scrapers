import re
from typing import IO, List

from boatrace.models.betting_method import BettingMethod
from boatrace.official.models import Payoff
from boatrace.official.v1707.scrapers.decorators import (
    no_content_handleable,
    race_cancellation_handleable,
)
from boatrace.official.v1707.scrapers.utils import parse_race_key_attributes
from bs4 import BeautifulSoup


@race_cancellation_handleable
@no_content_handleable
def scrape_race_payoff(file: IO) -> List[Payoff]:
    """レースの払い戻し情報をスクレイピングする

    Args:
        file (IO): レース結果のHTML

    Raises:
        ScrapingError:
        DataNotFound:

    Returns:
        List[PayOff]: パース結果を保持するデータモデル
    """
    soup = BeautifulSoup(file, "html.parser")
    race_key_attributes = parse_race_key_attributes(soup)
    race_holding_date = race_key_attributes["race_holding_date"]
    stadium_tel_code = race_key_attributes["stadium_tel_code"]
    race_number = race_key_attributes["race_number"]

    payment_table = soup.select(".table1")[3]
    # YAGNI原則に則って今の所三連単だけ対応
    trifecta_tbody = payment_table.select_one("tbody")
    rowspan = int(trifecta_tbody.select_one("td")["rowspan"])

    data = []
    for tr in trifecta_tbody.select("tr"):
        tds = tr.select(f'td:not([rowspan="{rowspan}"])')

        betting_numbers = tds[0].select("span.numberSet1_number")
        if len(betting_numbers) == 0:
            continue

        data.append(
            Payoff(
                race_holding_date=race_holding_date,
                stadium_tel_code=stadium_tel_code,
                race_number=race_number,
                betting_method=BettingMethod.TRIFECTA,
                betting_number=int(
                    "".join([span.get_text() for span in betting_numbers])
                ),
                amount=int(
                    re.match(r"¥([\d]+)", tds[1].get_text().replace(",", "")).group(1)
                ),
            )
        )

    return data
