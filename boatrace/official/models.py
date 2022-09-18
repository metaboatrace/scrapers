from dataclasses import dataclass
from datetime import date
from typing import Optional

from boatrace.models.betting_method import BettingMethod
from boatrace.models.branch import Branch
from boatrace.models.prefecture import Prefecture
from boatrace.models.racer_rank import RacerRank
from boatrace.models.stadium_tel_code import StadiumTelCode


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
class MotorPerformance:
    recorded_date: date
    number: int
    quinella_rate: Optional[float]
    trio_rate: Optional[float]
