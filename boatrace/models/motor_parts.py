from enum import Enum, auto


class MotorParts(Enum):
    ELECTRICAL_SYSTEM = auto()
    CARBURETOR = auto()
    PISTON = auto()
    PISTON_RING = auto()
    CYLINDER = auto()
    CRANKSHAFT = auto()
    GEAR_CASE = auto()
    CARRIER_BODY = auto()


class MotorPartsFactory:
    @staticmethod
    def create(name: str):
        if "電気" in name:
            return MotorParts.ELECTRICAL_SYSTEM
        elif "キャブ" in name:
            return MotorParts.CARBURETOR
        elif "ピストン" == name:
            return MotorParts.PISTON
        elif "リング" in name:
            return MotorParts.PISTON_RING
        elif "シリンダ" in name:
            return MotorParts.CYLINDER
        elif "ギア" in name:
            return MotorParts.GEAR_CASE
        elif "ギヤ" in name:
            return MotorParts.GEAR_CASE
        elif "キャリ" in name:
            return MotorParts.CARRIER_BODY
        else:
            raise ValueError
