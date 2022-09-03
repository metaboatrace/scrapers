import re
from dataclasses import dataclass
from datetime import date
from typing import IO, List

from boatrace.models.stadium_tel_code import StadiumTelCode
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
    start_course: int
    start_time: float
    exhibition_time: float


@no_content_handleable
@race_cancellation_handleable
def scrape_race_exhibition_records(file: IO) -> List[Dto]:
    soup = BeautifulSoup(file, "html.parser")
    race_key_attributes = parse_race_key_attributes(soup)

    data_fetching_from_exhibition_table = []
    for pit_number, row in enumerate(soup.select(".table1")[1].select("tbody"), 1):
        if "is-miss" in row["class"]:
            continue

        data_fetching_from_exhibition_table.append(
            {
                "pit_number": pit_number,
                "exhibition_time": float(row.select("td")[4].text),
            }
        )

    data_fetching_from_slit_table = []
    for start_course, row in enumerate(soup.select(".table1")[2].select("tbody tr"), 1):
        if m := re.search(r"_([1-6]{1}).png$", row.select_one("img")["src"]):
            pit_number = int(m.group(1))
        else:
            # 画像がない場合は出遅れか展示不出走
            #
            # 出遅れが発生した展示
            # http://boatrace.jp/owpc/pc/race/beforeinfo?rno=2&jcd=17&hd=20170511
            continue

        start_time_element = row.select("span")[-1]
        if m := re.search(r"F?\.(\d{2})$", start_time_element.text):
            start_time = float(f"0.{m.group(1)}")
        else:
            raise ValueError

        if "is-fBold" in start_time_element["class"]:
            # この場合はフライング
            start_time = start_time * -1

        data_fetching_from_slit_table.append(
            {
                "pit_number": pit_number,
                "start_course": start_course,
                "start_time": start_time,
            }
        )

    data = []
    for pit_number in range(1, 7):
        # todo: モジュール分割検討
        # 違和感感じる
        # スタート展示と周回展示とでDTOを分けた方がいいのでは？
        exhibition_data = (
            next(
                d
                for d in data_fetching_from_exhibition_table
                if d["pit_number"] == pit_number
            )
            or {}
        )
        slit_data = (
            next(
                d
                for d in data_fetching_from_slit_table
                if d["pit_number"] == pit_number
            )
            or {}
        )

        if exhibition_data or slit_data:
            data.append(
                Dto(**race_key_attributes, **dict(exhibition_data, **slit_data))
            )

    return data
