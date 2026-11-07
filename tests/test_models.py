from dataclasses import FrozenInstanceError
from datetime import date

import pytest

from trainingslog.models import Training, format_pace, geschwindigkeit_kmh, pace_min_pro_km


def lauf(km=10.0, minuten=55.0):
    return Training(date(2026, 10, 1), "Laufen", km, minuten)


def test_pace():
    assert pace_min_pro_km(lauf(10, 55)) == 5.5


def test_pace_bei_distanz_null():
    with pytest.raises(ValueError):
        pace_min_pro_km(lauf(km=0))


def test_geschwindigkeit():
    assert geschwindigkeit_kmh(lauf(10, 60)) == 10


def test_format_pace():
    assert format_pace(5.5) == "5:30 min/km"
    assert format_pace(4.0) == "4:00 min/km"


def test_from_row_normalisiert_werte():
    row = {"datum": "2026-10-01", "sportart": " laufen ", "distanz_km": "10",
           "dauer_min": "55", "hoehenmeter": "", "notiz": " Easy "}
    assert Training.from_row(row) == Training(date(2026, 10, 1), "Laufen", 10.0, 55.0, 0, "Easy")


def test_training_ist_unveraenderlich():
    t = lauf()
    with pytest.raises(FrozenInstanceError):
        t.notiz = "neu"


def test_with_note_erzeugt_kopie():
    t = lauf()
    neu = t.with_note("Intervalle")
    assert t.notiz == "" and neu.notiz == "Intervalle"
