from datetime import date

from trainingslog.models import Training
from trainingslog.storage import als_csv, lade_trainings, speichere_trainings

TRAININGS = (
    Training(date(2026, 10, 1), "Laufen", 10.0, 50.0, 80, "Easy"),
    Training(date(2026, 10, 2), "Velo", 42.5, 90.0),
)


def test_als_csv_ist_pure():
    assert als_csv(TRAININGS) == als_csv(TRAININGS)
    assert als_csv(()) == "datum,sportart,distanz_km,dauer_min,hoehenmeter,notiz\n"


def test_speichern_und_wieder_laden(tmp_path):
    pfad = tmp_path / "trainings.csv"
    speichere_trainings(pfad, TRAININGS)
    assert lade_trainings(pfad) == TRAININGS


def test_fehlende_datei_ergibt_leeres_tupel(tmp_path):
    assert lade_trainings(tmp_path / "gibts_nicht.csv") == ()
