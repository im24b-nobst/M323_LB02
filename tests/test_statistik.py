from datetime import date

import pytest

from app import app
from trainingslog.statistik import (bestleistungen, gruppiere_nach_sportart, km_pro_sportart,
                                    km_pro_woche, laengstes, schnellstes, top_laeufe)
from trainingslog.models import Training

LAUF_A = Training(date(2026, 10, 5), "Laufen", 10, 50)     # Mo KW41, Pace 5.0
LAUF_B = Training(date(2026, 10, 7), "Laufen", 21.1, 110)  # Mi KW41, Pace ~5.21
LAUF_C = Training(date(2026, 10, 12), "Laufen", 3, 12)     # KW42, Pace 4.0 aber < 5 km
VELO = Training(date(2026, 10, 13), "Velo", 60, 150)       # KW42
ALLE = (LAUF_A, LAUF_B, LAUF_C, VELO)


def test_km_pro_woche():
    assert km_pro_woche(ALLE) == {"2026-KW41": pytest.approx(31.1), "2026-KW42": 63.0}


def test_km_pro_woche_jahreswechsel():
    # 1. Januar 2027 gehoert zur ISO-Woche 53 von 2026
    assert km_pro_woche([Training(date(2027, 1, 1), "Laufen", 8, 40)]) == {"2026-KW53": 8.0}


def test_km_pro_sportart():
    assert km_pro_sportart(ALLE) == {"Laufen": pytest.approx(34.1), "Velo": 60.0}


def test_gruppieren():
    assert gruppiere_nach_sportart(ALLE) == {"Laufen": (LAUF_A, LAUF_B, LAUF_C), "Velo": (VELO,)}


def test_laengstes_und_schnellstes():
    laeufe = (LAUF_A, LAUF_B, LAUF_C)
    assert laengstes(laeufe) == LAUF_B
    assert schnellstes(laeufe) == LAUF_A          # LAUF_C ist kuerzer als 5 km


def test_schnellstes_ohne_kandidaten():
    assert schnellstes((LAUF_C,)) is None


def test_bestleistungen_komposition():
    assert bestleistungen(ALLE) == {
        "Laufen": {"laengstes": LAUF_B, "schnellstes": LAUF_A},
        "Velo": {"laengstes": VELO, "schnellstes": VELO},
    }


def test_bestleistungen_leer():
    assert bestleistungen(()) == {}


def test_top_laeufe_bei_gleicher_pace_laengerer_zuerst():
    kurz = Training(date(2026, 10, 1), "Laufen", 5, 25)     # Pace 5.0
    lang = Training(date(2026, 10, 2), "Laufen", 10, 50)    # Pace 5.0
    langsam = Training(date(2026, 10, 3), "Laufen", 8, 48)  # Pace 6.0
    assert top_laeufe([kurz, langsam, lang]) == (lang, kurz, langsam)
    assert top_laeufe([kurz, langsam, lang], anzahl=1) == (lang,)


def test_statistik_seite_ohne_daten(tmp_path):
    app.config.update(TESTING=True, DATA_FILE=tmp_path / "leer.csv")
    antwort = app.test_client().get("/statistik")
    assert antwort.status_code == 200
    assert "Keine Daten." in antwort.get_data(as_text=True)
