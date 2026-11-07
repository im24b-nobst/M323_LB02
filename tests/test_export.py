from app import app

CSV = """datum,sportart,distanz_km,dauer_min,hoehenmeter,notiz
2026-10-01,Laufen,10,50,80,Easy
2026-10-03,Velo,60,150,600,Ausfahrt
"""


def test_export_beruecksichtigt_filter(tmp_path):
    pfad = tmp_path / "trainings.csv"
    pfad.write_text(CSV, encoding="utf-8")
    app.config.update(TESTING=True, DATA_FILE=pfad)
    antwort = app.test_client().get("/export?sportart=Velo")
    assert antwort.mimetype == "text/csv"
    assert antwort.get_data(as_text=True) == (
        "datum,sportart,distanz_km,dauer_min,hoehenmeter,notiz\n"
        "2026-10-03,Velo,60,150,600,Ausfahrt\n"
    )
