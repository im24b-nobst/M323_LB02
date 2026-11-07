"""Misst drei Varianten von km_pro_woche.

Aufruf im Projektordner:  python -m benchmarks.bench_aggregation
"""
from __future__ import annotations

import random
import timeit
from collections import defaultdict
from datetime import date, timedelta
from functools import reduce

from trainingslog.models import SPORTARTEN, Training
from trainingslog.statistik import km_pro_woche, wochen_schluessel


# Variante A (alte Version aus Commit "Statistik-Seite"): reduce, kopiert das Dict bei jedem Training
def km_pro_woche_reduce_kopie(trainings):
    def addiere(summen, t):
        woche = wochen_schluessel(t)
        return {**summen, woche: summen.get(woche, 0.0) + t.distanz_km}
    return dict(sorted(reduce(addiere, trainings, {}).items()))


# Variante B: veraenderbares defaultdict, nur innerhalb der Funktion
def km_pro_woche_defaultdict(trainings):
    summen = defaultdict(float)
    for t in trainings:
        summen[wochen_schluessel(t)] += t.distanz_km
    return dict(sorted(summen.items()))


# Variante C = aktuelle Version im Projekt: sortieren + groupby (ohne Mutation)


def testdaten(anzahl: int) -> list[Training]:
    zufall = random.Random(42)
    start = date(2016, 1, 1)
    return [Training(start + timedelta(days=zufall.randrange(3650)), zufall.choice(SPORTARTEN),
                     round(zufall.uniform(3, 60), 1), zufall.uniform(20, 180))
            for _ in range(anzahl)]


def messe(name, funktion, daten, wiederholungen=5):
    sekunden = min(timeit.repeat(lambda: funktion(daten), number=1, repeat=wiederholungen))
    print(f"  {name:<28} {sekunden * 1000:9.1f} ms")


if __name__ == "__main__":
    for anzahl in (1_000, 10_000, 20_000):
        daten = testdaten(anzahl)
        assert km_pro_woche_reduce_kopie(daten).keys() == km_pro_woche(daten).keys()
        print(f"{anzahl} Trainings:")
        messe("A reduce + Dict-Kopie", km_pro_woche_reduce_kopie, daten)
        messe("B defaultdict (Mutation)", km_pro_woche_defaultdict, daten)
        messe("C sorted + groupby", km_pro_woche, daten)
