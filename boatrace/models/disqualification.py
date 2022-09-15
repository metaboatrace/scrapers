from enum import Enum, auto


class Disqualification(Enum):
    CAPSIZE = auto()
    FALL = auto()
    SINKING = auto()
    VIOLATION = auto()
    DISQUALIFICATION_AFTER_START = auto()
    ENGINE_STOP = auto()
    UNFINISHED = auto()
    REPAYMENT_OTHER_THAN_FLYING_AND_LATENESS = auto()
    FLYING = auto()
    LATENESS = auto()
    ABSENT = auto()


class DisqualificationFactory:
    @staticmethod
    def create(name: str):
        if "転" in name:
            return Disqualification.CAPSIZE
        elif "落" in name:
            return Disqualification.FALL
        elif "沈" in name:
            return Disqualification.SINKING
        elif "妨" in name:
            return Disqualification.VIOLATION
        elif "失" in name:
            return Disqualification.DISQUALIFICATION_AFTER_START
        elif "エ" in name:
            return Disqualification.ENGINE_STOP
        elif "不" in name:
            return Disqualification.UNFINISHED
        elif "返" in name:
            return Disqualification.REPAYMENT_OTHER_THAN_FLYING_AND_LATENESS
        elif "Ｆ" in name:
            return Disqualification.FLYING
        elif "Ｌ" in name:
            return Disqualification.LATENESS
        elif "欠" in name:
            return Disqualification.ABSENT
        elif "＿" in name:
            # NOTE: これは失格ではない
            # レース不成立で着順が定まらなかったケース
            # 例)
            # http://boatrace.jp/owpc/pc/race/raceresult?rno=11&jcd=23&hd=20170429
            # TODO:
            return None
        else:
            raise ValueError
