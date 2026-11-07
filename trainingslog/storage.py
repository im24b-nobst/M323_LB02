"""Lesen und Schreiben der CSV-Datei."""
from __future__ import annotations

import csv
from pathlib import Path

from .models import Training


def lade_trainings(pfad: Path) -> tuple[Training, ...]:
    if not pfad.exists():
        return ()
    with pfad.open(encoding="utf-8", newline="") as datei:
        return tuple(Training.from_row(row) for row in csv.DictReader(datei))
