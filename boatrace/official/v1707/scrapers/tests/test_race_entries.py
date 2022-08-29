import os
from datetime import date

from boatrace.models.racer_rank import RacerRank
from boatrace.models.stadium_tel_code import StadiumTelCode
from boatrace.official.models import RaceEntry
from boatrace.official.v1707.scrapers.race_entries import scrape_race_entries

base_path = os.path.dirname(os.path.abspath(__file__))


def test_scrape_race_entries():
    file_path = os.path.normpath(
        os.path.join(base_path, "./fixtures/race_information/20180301_07#_8R.html")
    )

    with open(file_path, mode="r") as file:
        data = scrape_race_entries(file)

    assert data == [
        RaceEntry(
            race_holding_date=date(2018, 3, 1),
            stadium_tel_code=StadiumTelCode.GAMAGORI,
            race_number=8,
            racer_registration_number=4190,
            racer_first_name="万記",
            racer_last_name="長嶋",
            current_racer_rating=RacerRank.A1,
            pit_number=1,
            is_absent=False,
            motor_number=66,
            boat_number=40,
        ),
        RaceEntry(
            race_holding_date=date(2018, 3, 1),
            stadium_tel_code=StadiumTelCode.GAMAGORI,
            race_number=8,
            racer_registration_number=4240,
            racer_first_name="裕梨",
            racer_last_name="今井",
            current_racer_rating=RacerRank.B1,
            pit_number=2,
            is_absent=False,
            motor_number=41,
            boat_number=43,
        ),
        RaceEntry(
            race_holding_date=date(2018, 3, 1),
            stadium_tel_code=StadiumTelCode.GAMAGORI,
            race_number=8,
            racer_registration_number=4419,
            racer_first_name="加央理",
            racer_last_name="原",
            current_racer_rating=RacerRank.B1,
            pit_number=3,
            is_absent=False,
            motor_number=58,
            boat_number=74,
        ),
        RaceEntry(
            race_holding_date=date(2018, 3, 1),
            stadium_tel_code=StadiumTelCode.GAMAGORI,
            race_number=8,
            racer_registration_number=3175,
            racer_first_name="千草",
            racer_last_name="渡辺",
            current_racer_rating=RacerRank.A2,
            pit_number=4,
            is_absent=False,
            motor_number=33,
            boat_number=13,
        ),
        RaceEntry(
            race_holding_date=date(2018, 3, 1),
            stadium_tel_code=StadiumTelCode.GAMAGORI,
            race_number=8,
            racer_registration_number=3254,
            racer_first_name="千春",
            racer_last_name="柳澤",
            current_racer_rating=RacerRank.B1,
            pit_number=5,
            is_absent=False,
            motor_number=71,
            boat_number=65,
        ),
        RaceEntry(
            race_holding_date=date(2018, 3, 1),
            stadium_tel_code=StadiumTelCode.GAMAGORI,
            race_number=8,
            racer_registration_number=4843,
            racer_first_name="巴恵",
            racer_last_name="深尾",
            current_racer_rating=RacerRank.B1,
            pit_number=6,
            is_absent=False,
            motor_number=40,
            boat_number=68,
        ),
    ]


def test_scrape_race_entries_including_absent():
    file_path = os.path.normpath(
        os.path.join(base_path, "./fixtures/race_information/20151116_03#_11R.html")
    )

    with open(file_path, mode="r") as file:
        data = scrape_race_entries(file)

    assert data == [
        RaceEntry(
            race_holding_date=date(2015, 11, 16),
            stadium_tel_code=StadiumTelCode.EDOGAWA,
            race_number=11,
            racer_registration_number=3872,
            racer_first_name="憲行",
            racer_last_name="岡田",
            current_racer_rating=RacerRank.A1,
            pit_number=1,
            is_absent=True,
            motor_number=62,
            boat_number=25,
        ),
        RaceEntry(
            race_holding_date=date(2015, 11, 16),
            stadium_tel_code=StadiumTelCode.EDOGAWA,
            race_number=11,
            racer_registration_number=3880,
            racer_first_name="宗孝",
            racer_last_name="浅見",
            current_racer_rating=RacerRank.B1,
            pit_number=2,
            is_absent=False,
            motor_number=61,
            boat_number=31,
        ),
        RaceEntry(
            race_holding_date=date(2015, 11, 16),
            stadium_tel_code=StadiumTelCode.EDOGAWA,
            race_number=11,
            racer_registration_number=3793,
            racer_first_name="真吾",
            racer_last_name="高橋",
            current_racer_rating=RacerRank.B1,
            pit_number=3,
            is_absent=False,
            motor_number=56,
            boat_number=60,
        ),
        RaceEntry(
            race_holding_date=date(2015, 11, 16),
            stadium_tel_code=StadiumTelCode.EDOGAWA,
            race_number=11,
            racer_registration_number=4357,
            racer_first_name="和也",
            racer_last_name="田中",
            current_racer_rating=RacerRank.A1,
            pit_number=4,
            is_absent=False,
            motor_number=68,
            boat_number=43,
        ),
        RaceEntry(
            race_holding_date=date(2015, 11, 16),
            stadium_tel_code=StadiumTelCode.EDOGAWA,
            race_number=11,
            racer_registration_number=4037,
            racer_first_name="正幸",
            racer_last_name="別府",
            current_racer_rating=RacerRank.A2,
            pit_number=5,
            is_absent=False,
            motor_number=26,
            boat_number=46,
        ),
        RaceEntry(
            race_holding_date=date(2015, 11, 16),
            stadium_tel_code=StadiumTelCode.EDOGAWA,
            race_number=11,
            racer_registration_number=3797,
            racer_first_name="繁",
            racer_last_name="岩井",
            current_racer_rating=RacerRank.A2,
            pit_number=6,
            is_absent=False,
            motor_number=20,
            boat_number=69,
        ),
    ]