"""Feature 1: CSV-Import.

Validierungsregeln sind Funktionen, die in einer Liste gespeichert sind.
map, filter und reduce werden je einzeln auf die Trainings angewendet.
"""
from __future__ import annotations

import csv
import io
from functools import reduce
from typing import Callable, Iterable

from .models import SPORTARTEN, Training

Regel = Callable[[Training], bool]


def distanz_positiv(t: Training) -> bool:
    return t.distanz_km > 0


def dauer_positiv(t: Training) -> bool:
    return t.dauer_min > 0


def bekannte_sportart(t: Training) -> bool:
    return t.sportart in SPORTARTEN


# Funktionen als Objekte: in einer Liste gespeichert und spaeter aufgerufen
VALIDIERUNGSREGELN: list[Regel] = [distanz_positiv, dauer_positiv, bekannte_sportart]


def ist_gueltig(t: Training, regeln: Iterable[Regel] = VALIDIERUNGSREGELN) -> bool:
    return all(regel(t) for regel in regeln)


def parse_row(row: dict[str, str]) -> Training | None:
    """Gibt None zurueck, wenn eine Zeile nicht gelesen werden kann."""
    try:
        return Training.from_row(row)
    except (KeyError, ValueError, AttributeError):
        return None


def ist_vorhanden(t: Training | None) -> bool:
    return t is not None


def import_csv(text: str) -> tuple[tuple[Training, ...], int]:
    """Liest CSV-Text ein. Rueckgabe: (gueltige Trainings, Anzahl verworfene Zeilen)."""
    zeilen = list(csv.DictReader(io.StringIO(text)))
    geparst = map(parse_row, zeilen)                                   # map
    lesbar = filter(ist_vorhanden, geparst)                            # filter
    gueltig = tuple(filter(ist_gueltig, lesbar))                       # filter mit Regel-Liste
    return gueltig, len(zeilen) - len(gueltig)


def total_distanz(trainings: Iterable[Training]) -> float:
    return reduce(lambda summe, t: summe + t.distanz_km, trainings, 0.0)  # reduce
