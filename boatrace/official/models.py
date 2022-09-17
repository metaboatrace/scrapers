from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional

from boatrace.models.betting_method import BettingMethod
from boatrace.models.branch import Branch
from boatrace.models.gender import Gender
from boatrace.models.prefecture import Prefecture
from boatrace.models.race_laps import RaceLaps
from boatrace.models.racer_rank import RacerRank
from boatrace.models.stadium_tel_code import StadiumTelCode


@dataclass(frozen=True)
class EventEntry:
    racer_registration_number: int
    racer_last_name: str
    racer_first_name: str
    racer_rank: RacerRank
    motor_number: int
    quinella_rate_of_motor: float
    boat_number: int
    quinella_rate_of_boat: float
    anterior_time: float
    racer_gender: Gender


@dataclass(frozen=True)
class RaceInformation:
    race_holding_date: date
    stadium_tel_code: StadiumTelCode
    race_number: int
    title: str
    race_laps: RaceLaps
    deadline_at: datetime
    is_course_fixed: bool
    use_stabilizer: bool


# note: 体重も級別も一応保持する
# 体重は節間日次で変動し、レースの直前情報でレース時の最新情報は取得できる
# 級別も成績に応じて期毎に改められる
# ただ、取得できるデータ（特にコストもかからないもの）は保持しておいた方がライブラリとしての汎用性が高くなるため持っておく
# 血液型は流石にいらないと思うので取ってない
@dataclass(frozen=True)
class Racer:
    last_name: str
    first_name: str
    registration_number: int
    birth_date: date
    height: int
    weight: float
    branch_prefecture: Branch
    born_prefecture: Prefecture
    term: int
    current_rating: RacerRank


@dataclass(frozen=True)
class Payoff:
    race_holding_date: date
    stadium_tel_code: StadiumTelCode
    race_number: int
    betting_method: BettingMethod
    betting_number: int
    amount: int


@dataclass(frozen=True)
class RaceEntry:
    race_holding_date: date
    stadium_tel_code: StadiumTelCode
    race_number: int
    racer_registration_number: int
    racer_first_name: str
    racer_last_name: str
    current_racer_rating: RacerRank
    pit_number: int  # todo: enum で持つべき？
    is_absent: bool
    motor_number: int
    boat_number: int


@dataclass(frozen=True)
class MotorPerformance:
    recorded_date: date
    number: int
    quinella_rate: Optional[float]
    trio_rate: Optional[float]


@dataclass(frozen=True)
class BoatPerformance:
    recorded_date: date
    number: int
    quinella_rate: Optional[float]
    trio_rate: Optional[float]
