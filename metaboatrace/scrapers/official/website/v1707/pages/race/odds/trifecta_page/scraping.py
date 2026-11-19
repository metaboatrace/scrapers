import re
from collections.abc import Iterator
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from functools import reduce
from itertools import zip_longest
from typing import IO

from bs4 import BeautifulSoup, ResultSet, Tag
from metaboatrace.models.race import BettingMethod, Odds

from metaboatrace.scrapers.official.website.exceptions import ScrapingError
from metaboatrace.scrapers.official.website.v1707.decorators import (
    no_content_handleable,
    race_cancellation_handleable,
)
from metaboatrace.scrapers.official.website.v1707.pages.race.utils import parse_race_key_attributes
from metaboatrace.scrapers.official.website.v1707.utils import jst_wall_clock_to_utc


class OddsPageStatus(Enum):
    """オッズページが、掲載しているオッズをどの段階の値として表示しているか.

    パリミュチュエル方式ではオッズが締切まで動くので、同じページ・同じ組番でも
    取得した時点で値の意味が変わる。値そのものからは区別できず、ページ上部の
    表示だけが手がかりになる。
    """

    PROVISIONAL = "provisional"
    """「オッズ更新時間 HH:MM」の表示。集計途中の値で、確定までにまだ動く.

    発売中に限らない。締切を過ぎても、集計が終わるまではこの表示のまま残る (締切 20:45 の
    レースで、20:45:20 の取得は「オッズ更新時間 20:44」、20:46:20 の取得は「締切時オッズ」
    だった)。したがってこの状態は「締切前に取得した」ことを意味しない。
    """

    FINAL = "final"
    """「締切時オッズ」の表示。発売票数の集計が終わった確定値で、以後変わらない."""


@dataclass(frozen=True)
class OddsPageState:
    status: OddsPageStatus
    odds_updated_at: datetime | None
    """ページが表示する「オッズ更新時間」 (UTC)。PROVISIONAL のときだけ値を持つ.

    ページを取得した時刻ではなく、公式サイトがオッズを最後に集計した時刻。分単位で
    しか表示されない。FINAL のページには時刻の表示が無いので None。
    """


def _grouper(
    n: int, iterable: ResultSet[Tag], fillvalue: Tag | None = None
) -> Iterator[tuple[Tag | None, ...]]:
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


@no_content_handleable
@race_cancellation_handleable
def extract_odds(file: IO[str]) -> list[Odds]:
    soup = BeautifulSoup(file, "html.parser")
    race_key_attributes = parse_race_key_attributes(soup)

    odds_table = soup.select(".table1")[1]
    if len(odds_table.select("tbody tr td.oddsPoint")) != 120:
        # 今の所三連単しか対応してないので、
        # オッズのページであっても三連単以外のファイルが渡されたらエラーとする
        raise TypeError

    second_arrived_cells = odds_table.select('tbody tr td[rowspan="4"]')
    second_arrived_numbers = reduce(
        lambda a, b: a + b,
        [
            [int(cell.text) for cell in cells if cell is not None] * 4
            for cells in _grouper(6, second_arrived_cells)
        ],
    )
    third_arrived_numbers = [
        int(td.text) for td in odds_table.select('tbody tr td[class^="is-boatColor"]')
    ]

    data = []
    for i, td in enumerate(odds_table.select("tbody tr td.oddsPoint"), 0):
        if td.text == "欠場":
            # データ自体を作らない
            # ratio を 0.0 にしてdtoを作ったりしてたこともあったが、0.0だとベットしたら0円になるってことだし
            # それも不自然なためデータ自体が作らないのが違和感がないため
            continue

        data.append(
            Odds(
                **race_key_attributes,
                betting_method=BettingMethod.TRIFECTA,
                betting_numbers=[(i % 6) + 1, second_arrived_numbers[i], third_arrived_numbers[i]],
                ratio=float(td.text),
            )
        )

    return data


@no_content_handleable
@race_cancellation_handleable
def extract_odds_page_state(file: IO[str]) -> OddsPageState:
    """オッズページ上部の表示から、掲載中のオッズの段階と更新時間を読む.

    ``extract_odds`` と同じ HTML に対して呼ぶ。オッズの値と組にして初めて
    「いつの時点の、確定前 / 確定後のオッズか」が決まる。

    どちらの表示も無いページは ``ScrapingError`` にする。段階を推測で埋めると、
    呼び出し側が暫定値を確定値として扱う取り違えを起こすため。
    """
    soup = BeautifulSoup(file, "html.parser")

    if (final_label := soup.select_one(".tab4_time")) and "締切時オッズ" in final_label.get_text():
        return OddsPageState(status=OddsPageStatus.FINAL, odds_updated_at=None)

    refresh_label = soup.select_one(".tab4_refreshText")
    if refresh_label is None or "オッズ更新時間" not in refresh_label.get_text():
        raise ScrapingError

    # 見出しだけあって時刻が空のページがある (観測したのはデータ無しのページで、そちらは
    # DataNotFound になる)。オッズが載っていて時刻だけ空でも段階は決まるので落とさない
    if not (m := re.search(r"(\d{1,2}):(\d{2})", refresh_label.get_text())):
        return OddsPageState(status=OddsPageStatus.PROVISIONAL, odds_updated_at=None)

    # 更新時間は開催日の HH:MM としてしか表示されない。レースは開催日の JST 暦日内に
    # 終わるので、開催日をそのまま暦日に使う
    race_holding_date = parse_race_key_attributes(soup)["race_holding_date"]
    return OddsPageState(
        status=OddsPageStatus.PROVISIONAL,
        odds_updated_at=jst_wall_clock_to_utc(race_holding_date, int(m.group(1)), int(m.group(2))),
    )
