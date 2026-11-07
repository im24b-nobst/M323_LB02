"""Testet die Filterseite ueber HTTP.

Diese Tests werden VOR dem Refactoring geschrieben und dürfen danach
nicht angepasst werden: so ist belegt, dass das Verhalten gleich bleibt.
"""
import re

import pytest

from app import app

CSV = """datum,sportart,distanz_km,dauer_min,hoehenmeter,notiz
2026-10-01,Laufen,10,50,80,Easy
2026-10-05,Laufen,21.1,110,150,Halbmarathon
2026-10-03,Velo,60,150,600,Ausfahrt
2026-09-20,Laufen,5,30,20,Kurz
"""


@pytest.fixture
def client(tmp_path):
    pfad = tmp_path / "trainings.csv"
    pfad.write_text(CSV, encoding="utf-8")
    app.config.update(TESTING=True, DATA_FILE=pfad)
    return app.test_client()


def daten_in_tabelle(html: str) -> list[str]:
    return re.findall(r'<tr class="training">\s*<td>([\d-]+)</td>', html)


def zusammenfassung(html: str) -> str:
    return re.search(r'<p id="zusammenfassung">(.*?)</p>', html).group(1)


def test_ohne_filter_alle_neueste_zuerst(client):
    html = client.get("/trainings").get_data(as_text=True)
    assert daten_in_tabelle(html) == ["2026-10-05", "2026-10-03", "2026-10-01", "2026-09-20"]
    assert "Total: 96.1 km" in zusammenfassung(html)


def test_filter_sportart(client):
    html = client.get("/trainings?sportart=Laufen").get_data(as_text=True)
    assert daten_in_tabelle(html) == ["2026-10-05", "2026-10-01", "2026-09-20"]
    assert "3 Trainings" in zusammenfassung(html)


def test_filter_zeitraum_und_mindestdistanz(client):
    html = client.get("/trainings?von=2026-10-01&bis=2026-10-31&min_km=10").get_data(as_text=True)
    assert daten_in_tabelle(html) == ["2026-10-05", "2026-10-03", "2026-10-01"]


def test_sortierung_nach_distanz(client):
    html = client.get("/trainings?sort=distanz").get_data(as_text=True)
    assert daten_in_tabelle(html) == ["2026-10-03", "2026-10-05", "2026-10-01", "2026-09-20"]


def test_durchschnittspace(client):
    # Paces: 5.0 und 6.0 min/km -> Durchschnitt 5.5 = 5:30
    html = client.get("/trainings?sportart=Laufen&bis=2026-10-01").get_data(as_text=True)
    assert "Ø Pace: 5:30 min/km" in zusammenfassung(html)


def test_kein_treffer(client):
    html = client.get("/trainings?sportart=Schwimmen").get_data(as_text=True)
    assert daten_in_tabelle(html) == []
    assert "Ø Pace: -" in zusammenfassung(html)
    assert "Keine Trainings gefunden" in html
