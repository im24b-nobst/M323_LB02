from datetime import date

import pytest

from trainingslog.importer import (VALIDIERUNGSREGELN, bekannte_sportart, import_csv,
                                   ist_gueltig, total_distanz)
from trainingslog.models import Training

HEADER = "datum,sportart,distanz_km,dauer_min,hoehenmeter,notiz\n"


def test_gueltige_zeile_wird_importiert():
    trainings, verworfen = import_csv(HEADER + "2026-10-01,laufen,10,50,80,Easy\n")
    assert verworfen == 0
    assert trainings == (Training(date(2026, 10, 1), "Laufen", 10.0, 50.0, 80, "Easy"),)


def test_ungueltige_zeilen_werden_verworfen():
    text = HEADER + (
        "2026-10-01,Laufen,10,50,0,\n"
        "kein-datum,Laufen,5,30,0,\n"     # Datum nicht lesbar
        "2026-10-02,Laufen,0,30,0,\n"     # Distanz 0
        "2026-10-03,Curling,5,30,0,\n"    # unbekannte Sportart
    )
    trainings, verworfen = import_csv(text)
    assert len(trainings) == 1
    assert verworfen == 3


def test_leere_datei():
    assert import_csv(HEADER) == ((), 0)


def test_regeln_sind_funktionen_in_einer_liste():
    curling = Training(date(2026, 10, 1), "Curling", 5, 30)
    assert bekannte_sportart in VALIDIERUNGSREGELN
    assert not ist_gueltig(curling)
    assert ist_gueltig(curling, regeln=[])          # ohne Regeln ist alles gueltig


def test_total_distanz():
    trainings, _ = import_csv(HEADER + "2026-10-01,Laufen,10,50,,\n2026-10-02,Velo,42.5,90,,\n")
    assert total_distanz(trainings) == pytest.approx(52.5)
    assert total_distanz(()) == 0
