# Trainingslog

Flask-App zum Auswerten von Ausdauertrainings (Laufen, Velo, Schwimmen, Wandern).
Praxisprojekt Modul 323 – Funktional Programmieren.

## Starten

```bash
python -m venv .venv
.venv\Scripts\activate          # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python app.py                   # http://127.0.0.1:5000
pytest                          # alle Tests
python -m benchmarks.bench_aggregation   # Performance-Messung
```

## Features

| Seite | Was sie macht | Code |
|---|---|---|
| `/` | letzte 10 Trainings | `app.py` |
| `/import` | CSV hochladen, Zeilen pruefen und speichern | `trainingslog/importer.py` |
| `/trainings` | filtern nach Sportart, Zeitraum, Mindestdistanz; sortieren | `trainingslog/filters.py` |
| `/export` | gefilterte Trainings als CSV herunterladen | `trainingslog/storage.py` |
| `/statistik` | km pro Woche / Sportart, Bestleistungen, Top 5 Laeufe | `trainingslog/statistik.py` |

## Wo welches Kompetenzfeld belegt ist

| Feld | Datei / Commit |
|---|---|
| A1B | `storage.py`: `als_csv` (pure) neben `speichere_trainings` (Prozedur) |
| A1I | `models.py`: frozen `Training` + `with_note`; Commit "Filterseite imperativ" (`append`, `sort`) vs. `filters.py` |
| A1A | `paradigmen.py` |
| B1B | `models.py` (immutable type, constructor `from_row`), `filters.py` (`alle`) |
| B1I | `docs/design_statistik.md` |
| B1A | Commits "Filterseite imperativ" -> "Filterseite deklarativ" |
| C1B / C1I / C1A | `statistik.py`: `bestleistungen` und Teilfunktionen, `tests/test_statistik.py` |
| C2B | Feature Import: `importer.py` |
| C2I | Feature Filter: `filters.py` |
| C2A | Feature Statistik: `statistik.py` (`gruppiere`, `km_pro_woche`, `top_laeufe`) |
| D1B | Refactorings in den Commits 5 und 8, Performance in 8 und 9 |
| D1I | Commits "Filterseite imperativ" -> "Filterseite deklarativ", `tests/test_trainings_route.py` |
| D1A | `benchmarks/bench_aggregation.py` |
