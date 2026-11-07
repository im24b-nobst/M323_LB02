"""Feature 3: Statistik – Aggregation und benutzerdefinierte Sortierung."""
from __future__ import annotations

from functools import reduce
from typing import Iterable

from .models import Training, pace_min_pro_km

MIN_KM_FUER_PACE = 5.0


# --- Aggregation ---

def wochen_schluessel(t: Training) -> str:
    jahr, woche, _ = t.datum.isocalendar()
    return f"{jahr}-KW{woche:02d}"


def km_pro_woche(trainings: Iterable[Training]) -> dict[str, float]:
    def addiere(summen: dict[str, float], t: Training) -> dict[str, float]:
        woche = wochen_schluessel(t)
        return {**summen, woche: summen.get(woche, 0.0) + t.distanz_km}
    return dict(sorted(reduce(addiere, trainings, {}).items()))


def km_pro_sportart(trainings: Iterable[Training]) -> dict[str, float]:
    def addiere(summen: dict[str, float], t: Training) -> dict[str, float]:
        return {**summen, t.sportart: summen.get(t.sportart, 0.0) + t.distanz_km}
    return reduce(addiere, trainings, {})


# --- Algorithmus Bestleistungen (in Teilfunktionen zerlegt) ---

def gruppiere_nach_sportart(trainings: Iterable[Training]) -> dict[str, tuple[Training, ...]]:
    gruppen: dict[str, tuple[Training, ...]] = {}
    for t in trainings:
        gruppen[t.sportart] = gruppen.get(t.sportart, ()) + (t,)
    return gruppen


def laengstes(trainings: tuple[Training, ...]) -> Training:
    return max(trainings, key=lambda t: t.distanz_km)


def schnellstes(trainings: tuple[Training, ...], min_km: float = MIN_KM_FUER_PACE) -> Training | None:
    kandidaten = tuple(filter(lambda t: t.distanz_km >= min_km, trainings))
    return min(kandidaten, key=pace_min_pro_km) if kandidaten else None


def bestleistungen(trainings: Iterable[Training]) -> dict[str, dict[str, Training | None]]:
    """Komposition: gruppieren -> pro Gruppe laengstes und schnellstes bestimmen."""
    return {
        sportart: {"laengstes": laengstes(gruppe), "schnellstes": schnellstes(gruppe)}
        for sportart, gruppe in sorted(gruppiere_nach_sportart(trainings).items())
    }


# --- Benutzerdefinierte Sortierung ---

def schnellste_zuerst(t: Training) -> tuple[float, float]:
    """Sortierschluessel: zuerst nach Pace aufsteigend, bei Gleichstand laengere Distanz zuerst."""
    return (pace_min_pro_km(t), -t.distanz_km)


def top_laeufe(trainings: Iterable[Training], anzahl: int = 5) -> tuple[Training, ...]:
    laeufe = filter(lambda t: t.sportart == "Laufen" and t.distanz_km >= MIN_KM_FUER_PACE, trainings)
    return tuple(sorted(laeufe, key=schnellste_zuerst)[:anzahl])
