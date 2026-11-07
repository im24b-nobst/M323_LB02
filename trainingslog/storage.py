"""Lesen und Schreiben der CSV-Datei."""
from __future__ import annotations

import csv
import io
from functools import lru_cache
from pathlib import Path
from typing import Iterable

from .models import CSV_FELDER, Training


def lade_trainings(pfad: Path) -> tuple[Training, ...]:
    if not pfad.exists():
        return ()
    info = pfad.stat()
    return _lade_cached(pfad, info.st_mtime_ns, info.st_size)


@lru_cache(maxsize=8)
def _lade_cached(pfad: Path, geaendert_ns: int, groesse: int) -> tuple[Training, ...]:
    """Liest die Datei nur neu, wenn sich Zeitstempel oder Groesse geaendert haben.

    Caching ist hier sicher, weil das Resultat unveraenderlich ist (Tupel aus frozen dataclasses).
    """
    with pfad.open(encoding="utf-8", newline="") as datei:
        return tuple(Training.from_row(row) for row in csv.DictReader(datei))


def als_csv(trainings: Iterable[Training]) -> str:
    """Pure function: macht aus Trainings einen CSV-Text, ohne etwas zu veraendern."""
    puffer = io.StringIO()
    writer = csv.DictWriter(puffer, fieldnames=CSV_FELDER, lineterminator="\n")
    writer.writeheader()
    writer.writerows(t.to_row() for t in trainings)
    return puffer.getvalue()


def speichere_trainings(pfad: Path, trainings: Iterable[Training]) -> None:
    """Prozedur: schreibt die Datei (Seiteneffekt) und gibt nichts zurueck."""
    pfad.parent.mkdir(parents=True, exist_ok=True)
    pfad.write_text(als_csv(trainings), encoding="utf-8")
    _lade_cached.cache_clear()
