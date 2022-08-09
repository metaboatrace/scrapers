from dataclasses import dataclass
from datetime import date

from boatrace.models.gender import Gender
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


@dataclass(frozen=True)
class EventEntry:
    racer_registration_number: int
    racer_last_name: str
    racer_first_name: str
    racer_rank: RaceGrade
    motor_number: int
    quinella_rate_of_motor: float
    boat_number: int
    quinella_rate_of_boat: float
    anterior_time: float
    racer_gender: Gender
