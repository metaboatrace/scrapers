from enum import Enum, auto


class WinningTrick(Enum):
    NIGE = auto()
    SASHI = auto()
    MAKURI = auto()
    MAKURIZASHI = auto()
    NUKI = auto()
    MEGUMARE = auto()


class WinningTrickFactory:
    @staticmethod
    def create(name: str):
        if "逃げ" == name:
            return WinningTrick.NIGE
        elif "差し" == name:
            return WinningTrick.SASHI
        elif "まくり" == name:
            return WinningTrick.MAKURI
        elif "まくり差し" == name:
            return WinningTrick.MAKURIZASHI
        elif "抜き" == name:
            return WinningTrick.NUKI
        elif "恵まれ" == name:
            return WinningTrick.MEGUMARE
        else:
            raise ValueError
