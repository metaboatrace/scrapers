from enum import Enum, auto


class Weather(Enum):
    FINE = auto()
    CLOUDY = auto()
    RAINY = auto()
    SNOWY = auto()
    TYPHOON = auto()
    FOG = auto()


class WeatherFactory:
    @staticmethod
    def create(name: str):
        if "晴" in name:
            return Weather.FINE
        elif "曇" in name:
            return Weather.CLOUDY
        elif "雨" in name:
            return Weather.RAINY
        elif "雪" in name:
            return Weather.SNOWY
        elif "台風" in name:
            return Weather.TYPHOON
        elif "霧" in name:
            return Weather.FOG
        else:
            raise ValueError
