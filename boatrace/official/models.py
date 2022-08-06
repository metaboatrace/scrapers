from dataclasses import dataclass
from datetime import date

from boatrace.models.race_grade import RaceGrade
from boatrace.models.race_kind import RaceKind


@dataclass(frozen=True)
class Event:
    stadium_tel_code: int
    title: str
    starts_on: date
    days: int
    grade: RaceGrade
    kind: RaceKind
