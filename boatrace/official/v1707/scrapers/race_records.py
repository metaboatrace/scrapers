import re
import unicodedata
from dataclasses import dataclass
from datetime import date
from typing import IO, Optional

import numpy as np
from boatrace.models.disqualification import Disqualification, DisqualificationFactory
from boatrace.models.stadium_tel_code import StadiumTelCode
from boatrace.models.winning_trick import WinningTrick, WinningTrickFactory
from boatrace.official.v1707.scrapers.decorators import (
    no_content_handleable,
    race_cancellation_handleable,
)
from boatrace.official.v1707.scrapers.utils import parse_race_key_attributes
from bs4 import BeautifulSoup


@dataclass(frozen=True)
class Dto:
    race_holding_date: date
    stadium_tel_code: StadiumTelCode
    race_number: int
    pit_number: int
    start_course: Optional[int] = None
    arrival: Optional[int] = None
    total_time: Optional[float] = None
    start_time: Optional[float] = None
    winning_trick: Optional[WinningTrick] = None
    disqualification: Optional[Disqualification] = None


@no_content_handleable
@race_cancellation_handleable
def scrape_race_records(file: IO) -> Dto:
    soup = BeautifulSoup(file, "html.parser")
    race_key_attributes = parse_race_key_attributes(soup)

    # データがテーブル横断で存在しているため分けてとる
    # これは順位のテーブル
    data_originated_record_table = []
    for row in soup.select(".table1")[1].select("tbody"):
        pit_number = int(row.select("td")[1].text)

        arrival_mark = row.select("td")[0].text
        try:
            arrival = int(unicodedata.normalize("NFKC", arrival_mark))
            disqualification = None
        except ValueError:
            # note: 失格はレース不成立で着順が定まらなかったケースにNoneになり得る
            arrival = None
            disqualification = DisqualificationFactory.create(arrival_mark)

        time_text = row.select("td")[3].text
        if m := re.search(r'(\d{1})\'(\d{2})"(\d{1})', time_text):
            total_time = (
                60 * int(m.group(1)) + 1 * int(m.group(2)) + 0.1 * int(m.group(3))
            )
        else:
            total_time = None

        data_originated_record_table.append(
            {
                "pit_number": pit_number,
                "arrival": arrival,
                "total_time": total_time,
                "disqualification": disqualification,
            }
        )

    # ここからはスリットのテーブル
    data_originated_slit_table = []
    for start_course, row in enumerate(soup.select(".table1")[2].select("tbody tr"), 1):
        pit_number = int(row.select_one(".table1_boatImage1Number").text)

        time_text = row.select_one(".table1_boatImage1TimeInner").text.strip()
        if m := re.search(r"([\u4E00-\u9FD0あ-ん]+)", time_text):
            winning_trick = WinningTrickFactory.create(m.group(1))
        else:
            winning_trick = None

        if m := re.search(r"(F?)\.(\d{1,2})", time_text):
            start_time = float(f"0.{m.group(2)}")
            if m.group(1):
                # フライングは負の数で返す
                # disqualification でフライングかどうかはわかるが、正常なスタートと同じ値で返すのは違和感あるため
                start_time = start_time * -1
        else:
            # 出遅れはこの表に表示されないし、フライングの場合はF記号がついて表示されるので取れないケースはないはず
            raise ValueError

        data_originated_slit_table.append(
            {
                "pit_number": pit_number,
                "start_course": start_course,
                "start_time": start_time,
                "winning_trick": winning_trick,
            }
        )

    # 表別に取っておいたデータをマージする
    data = [
        Dto(
            **dict(
                race_key_attributes,
                **dict(
                    next(
                        (
                            d
                            for d in data_originated_record_table
                            if d.get("pit_number") == pit_number
                        ),
                        {},
                    ),
                    **next(
                        (
                            d
                            for d in data_originated_slit_table
                            if d.get("pit_number") == pit_number
                        ),
                        {},
                    ),
                ),
            )
        )
        for pit_number in range(1, 7)
    ]

    return data
