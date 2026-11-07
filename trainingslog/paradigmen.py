"""Dieselbe Aufgabe in drei Paradigmen: Gesamt-Kilometer pro Sportart.

Die funktionale Variante ist km_pro_sportart() in statistik.py und wird von der
Statistik-Seite verwendet. Die beiden anderen Varianten dienen dem Vergleich.
"""
from __future__ import annotations

from typing import Iterable

from .models import Training
from .statistik import km_pro_sportart  # funktionale Variante


# --- Prozedural: Schritt fuer Schritt, Zwischenstand in einer veraenderbaren Variable ---

def km_pro_sportart_prozedural(trainings: Iterable[Training]) -> dict[str, float]:
    summen = {}
    for t in trainings:
        if t.sportart not in summen:
            summen[t.sportart] = 0.0
        summen[t.sportart] += t.distanz_km
    return summen


# --- Objektorientiert: Zustand und Verhalten in einem Objekt ---

class Trainingsbuch:
    def __init__(self) -> None:
        self._summen: dict[str, float] = {}

    def erfasse(self, t: Training) -> None:
        self._summen[t.sportart] = self._summen.get(t.sportart, 0.0) + t.distanz_km

    def km_pro_sportart(self) -> dict[str, float]:
        return dict(self._summen)


def km_pro_sportart_oo(trainings: Iterable[Training]) -> dict[str, float]:
    buch = Trainingsbuch()
    for t in trainings:
        buch.erfasse(t)
    return buch.km_pro_sportart()


__all__ = ["km_pro_sportart", "km_pro_sportart_prozedural", "km_pro_sportart_oo", "Trainingsbuch"]
