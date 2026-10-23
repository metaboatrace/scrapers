from collections.abc import Iterator
from dataclasses import dataclass
from typing import IO

from bs4 import BeautifulSoup, Tag
from metaboatrace.models.racer import Gender, Racer, RacerRank

from metaboatrace.scrapers.official.website.v1707.decorators import no_content_handleable
from metaboatrace.scrapers.official.website.v1707.utils import split_racer_name


@dataclass(frozen=True)
class EventEntry:
    racer_registration_number: int
    racer_gender: Gender
    racer_last_name: str
    racer_first_name: str
    racer_rank: RacerRank
    motor_number: int
    quinella_rate_of_motor: float
    boat_number: int
    quinella_rate_of_boat: float
    anterior_time: float


@dataclass(frozen=True)
class _EntryRacer:
    """前検情報テーブルの 1 行から読めるレーサー属性。Racer / EventEntry の両方の材料になる."""

    registration_number: int
    gender: Gender
    last_name: str
    first_name: str
    rank: RacerRank


def _iter_entry_rows(soup: BeautifulSoup) -> Iterator[tuple[Tag, _EntryRacer]]:
    """前検情報テーブルの各行と、そこから読んだレーサー属性 (両 extractor 共通部分) を返す."""
    for row in soup.select(".table1 table tbody tr"):
        cells = row.select("td")
        racer_last_name, racer_first_name = split_racer_name(cells[2].get_text())
        yield (
            row,
            _EntryRacer(
                registration_number=int(cells[1].get_text()),
                gender=Gender.FEMALE if row.select_one("i.is-lady") else Gender.MALE,
                last_name=racer_last_name,
                first_name=racer_first_name,
                rank=RacerRank.from_string(cells[3].get_text().strip()),
            ),
        )


@no_content_handleable
def extract_racers(file: IO[str]) -> list[Racer]:
    soup = BeautifulSoup(file, "html.parser")

    return [
        Racer(
            registration_number=racer.registration_number,
            last_name=racer.last_name,
            first_name=racer.first_name,
            gender=racer.gender,
            current_rating=racer.rank,
        )
        for _, racer in _iter_entry_rows(soup)
    ]


@no_content_handleable
def extract_event_entries(file: IO[str]) -> list[EventEntry]:
    soup = BeautifulSoup(file, "html.parser")

    data = []
    for row, racer in _iter_entry_rows(soup):
        cells = row.select("td")
        data.append(
            EventEntry(
                racer_registration_number=racer.registration_number,
                racer_gender=racer.gender,
                racer_last_name=racer.last_name,
                racer_first_name=racer.first_name,
                racer_rank=racer.rank,
                motor_number=int(cells[4].get_text().strip()),
                quinella_rate_of_motor=float(cells[5].get_text().strip()[:-1]),
                boat_number=int(cells[6].get_text().strip()),
                quinella_rate_of_boat=float(cells[7].get_text().strip()[:-1]),
                anterior_time=float(cells[8].get_text().strip()),
            )
        )

    return data
