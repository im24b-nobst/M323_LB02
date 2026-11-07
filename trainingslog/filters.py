"""Feature 2: Suche/Filter – deklarativ mit kombinierbaren Filtern.

Jeder Filter ist eine Funktion Training -> bool (ein "Praedikat").
Filter werden mit alle(...) zu einem einzigen Filter kombiniert.
"""
from __future__ import annotations

from datetime import date
from functools import reduce
from typing import Callable, Iterable, Mapping

from .models import Training, format_pace, pace_min_pro_km

Praedikat = Callable[[Training], bool]


# --- Filter-Fabriken: geben eine Funktion zurueck (Lambda) ---

def nach_sportart(sportart: str) -> Praedikat:
    return lambda t: t.sportart == sportart


def ab_datum(von: date) -> Praedikat:
    return lambda t: t.datum >= von


def bis_datum(bis: date) -> Praedikat:
    return lambda t: t.datum <= bis


def mindestens_km(km: float) -> Praedikat:
    return lambda t: t.distanz_km >= km


def alle(*praedikate: Praedikat) -> Praedikat:
    """Composable operator: verbindet beliebig viele Filter mit UND."""
    return lambda t: all(p(t) for p in praedikate)


# Formularfeld -> Funktion, die aus dem Text den passenden Filter baut
FILTER_AUS_FORMULAR: dict[str, Callable[[str], Praedikat]] = {
    "sportart": nach_sportart,
    "von": lambda wert: ab_datum(date.fromisoformat(wert)),
    "bis": lambda wert: bis_datum(date.fromisoformat(wert)),
    "min_km": lambda wert: mindestens_km(float(wert)),
}

SORTIERUNGEN: dict[str, Callable[[Training], object]] = {
    "datum": lambda t: t.datum,
    "distanz": lambda t: t.distanz_km,
}


def filter_aus_formular(args: Mapping[str, str]) -> Praedikat:
    return alle(*(baue(args[feld]) for feld, baue in FILTER_AUS_FORMULAR.items() if args.get(feld)))


def filtere_und_sortiere(trainings: Iterable[Training], args: Mapping[str, str]) -> tuple[Training, ...]:
    schluessel = SORTIERUNGEN.get(args.get("sort", ""), SORTIERUNGEN["datum"])
    return tuple(sorted(filter(filter_aus_formular(args), trainings), key=schluessel, reverse=True))


def kennzahlen(trainings: tuple[Training, ...]) -> dict[str, object]:
    """Verkettet map und reduce: Total-km und Durchschnittspace."""
    total_km = reduce(lambda summe, km: summe + km, map(lambda t: t.distanz_km, trainings), 0.0)
    summe_pace = reduce(lambda summe, p: summe + p, map(pace_min_pro_km, trainings), 0.0)
    return {
        "anzahl": len(trainings),
        "total_km": total_km,
        "durchschnitt_pace": format_pace(summe_pace / len(trainings)) if trainings else "-",
    }
