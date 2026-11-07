from datetime import date

from trainingslog.filters import (alle, filtere_und_sortiere, kennzahlen, mindestens_km,
                                  nach_sportart)
from trainingslog.models import Training

LAUF_10 = Training(date(2026, 10, 1), "Laufen", 10, 50)
LAUF_5 = Training(date(2026, 10, 2), "Laufen", 5, 30)
VELO_60 = Training(date(2026, 10, 3), "Velo", 60, 150)
ALLE = (LAUF_10, LAUF_5, VELO_60)


def test_filter_sind_kombinierbar():
    lange_laeufe = alle(nach_sportart("Laufen"), mindestens_km(8))
    assert tuple(filter(lange_laeufe, ALLE)) == (LAUF_10,)


def test_alle_ohne_filter_laesst_alles_durch():
    assert tuple(filter(alle(), ALLE)) == ALLE


def test_filtere_und_sortiere_veraendert_eingabe_nicht():
    eingabe = [LAUF_10, LAUF_5, VELO_60]
    resultat = filtere_und_sortiere(eingabe, {"sort": "distanz"})
    assert resultat == (VELO_60, LAUF_10, LAUF_5)
    assert eingabe == [LAUF_10, LAUF_5, VELO_60]


def test_kennzahlen():
    k = kennzahlen((LAUF_10, LAUF_5))
    assert k == {"anzahl": 2, "total_km": 15.0, "durchschnitt_pace": "5:30 min/km"}


def test_kennzahlen_leer():
    assert kennzahlen(()) == {"anzahl": 0, "total_km": 0.0, "durchschnitt_pace": "-"}
