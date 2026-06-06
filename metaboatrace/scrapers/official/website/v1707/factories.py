from typing import Literal, cast

from metaboatrace.models.boat import MotorParts
from metaboatrace.models.race import Disqualification, Weather, WinningTrick
from metaboatrace.models.stadium import EventHoldingStatus


class DisqualificationFactory:
    @staticmethod
    def create(name: str) -> Disqualification | None:
        if "転" in name:
            return Disqualification.CAPSIZE
        if "落" in name:
            return Disqualification.FALL
        if "沈" in name:
            return Disqualification.SINKING
        if "妨" in name:
            return Disqualification.VIOLATION
        if "失" in name:
            return Disqualification.DISQUALIFICATION_AFTER_START
        if "エ" in name:
            return Disqualification.ENGINE_STOP
        if "不" in name:
            return Disqualification.UNFINISHED
        if "返" in name:
            return Disqualification.REPAYMENT_OTHER_THAN_FLYING_AND_LATENESS
        if "Ｆ" in name:
            return Disqualification.FLYING
        if "Ｌ" in name:
            return Disqualification.LATENESS
        if "欠" in name:
            return Disqualification.ABSENT
        if "＿" in name:
            # 失格ではなく、レース不成立で着順が定まらなかったケース
            # 例) http://boatrace.jp/owpc/pc/race/raceresult?rno=11&jcd=23&hd=20170429
            return None
        if "　" in name:
            # 失格ではなく、レース不成立で着順が定まらなかったケース
            # 例) https://boatrace.jp/owpc/pc/race/raceresult?rno=2&jcd=23&hd=20160507
            return None
        raise ValueError


class MotorPartsFactory:
    @staticmethod
    def create(name: str) -> MotorParts:
        if "電気" in name:
            return MotorParts.ELECTRICAL_SYSTEM
        if "キャブ" in name:
            return MotorParts.CARBURETOR
        if name == "ピストン":
            return MotorParts.PISTON
        if "リング" in name:
            return MotorParts.PISTON_RING
        if "シリンダ" in name:
            return MotorParts.CYLINDER
        if "ギア" in name or "ギヤ" in name:
            return MotorParts.GEAR_CASE
        if "キャリ" in name:
            return MotorParts.CARRIER_BODY
        if "シャフト" in name:
            return MotorParts.CRANKSHAFT
        raise ValueError


class RaceLapsFactory:
    METRE_PER_A_LAP = 600

    @classmethod
    def create(cls, metre: Literal[1200, 1800]) -> Literal[2, 3]:
        return cast(Literal[2, 3], metre // cls.METRE_PER_A_LAP)


class WinningTrickFactory:
    @staticmethod
    def create(name: str) -> WinningTrick:
        if name == "逃げ":
            return WinningTrick.NIGE
        if name == "差し":
            return WinningTrick.SASHI
        if name == "まくり":
            return WinningTrick.MAKURI
        if name == "まくり差し":
            return WinningTrick.MAKURIZASHI
        if name == "抜き":
            return WinningTrick.NUKI
        if name == "恵まれ":
            return WinningTrick.MEGUMARE
        raise ValueError


class WeatherFactory:
    @staticmethod
    def create(name: str) -> Weather:
        if "晴" in name:
            return Weather.FINE
        if "曇" in name:
            return Weather.CLOUDY
        if "雨" in name:
            return Weather.RAINY
        if "雪" in name:
            return Weather.SNOWY
        if "台風" in name:
            return Weather.TYPHOON
        if "霧" in name:
            return Weather.FOG
        raise ValueError


class EventHoldingStatusFactory:
    @staticmethod
    def create(text: str) -> Weather:
        if text == "中止":
            return EventHoldingStatus.CANCELED
        if text == "中止順延":
            return EventHoldingStatus.POSTPONED
        return EventHoldingStatus.OPEN
