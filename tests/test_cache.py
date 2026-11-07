from datetime import date

from trainingslog.models import Training
from trainingslog.storage import _lade_cached, lade_trainings, speichere_trainings

LAUF = Training(date(2026, 10, 1), "Laufen", 10.0, 50.0)
VELO = Training(date(2026, 10, 2), "Velo", 40.0, 90.0)


def test_zweiter_aufruf_kommt_aus_dem_cache(tmp_path):
    pfad = tmp_path / "trainings.csv"
    speichere_trainings(pfad, [LAUF])
    lade_trainings(pfad)
    treffer_vorher = _lade_cached.cache_info().hits
    lade_trainings(pfad)
    assert _lade_cached.cache_info().hits == treffer_vorher + 1


def test_nach_dem_speichern_werden_neue_daten_geladen(tmp_path):
    pfad = tmp_path / "trainings.csv"
    speichere_trainings(pfad, [LAUF])
    assert lade_trainings(pfad) == (LAUF,)
    speichere_trainings(pfad, [LAUF, VELO])
    assert lade_trainings(pfad) == (LAUF, VELO)
