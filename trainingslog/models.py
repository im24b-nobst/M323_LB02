"""Datenmodell: ein Training ist ein unveraenderlicher Wert."""
from __future__ import annotations

from dataclasses import dataclass, replace
from datetime import date

SPORTARTEN = ("Laufen", "Velo", "Schwimmen", "Wandern")
CSV_FELDER = ("datum", "sportart", "distanz_km", "dauer_min", "hoehenmeter", "notiz")


@dataclass(frozen=True)
class Training:
    datum: date
    sportart: str
    distanz_km: float
    dauer_min: float
    hoehenmeter: int = 0
    notiz: str = ""

    @classmethod
    def from_row(cls, row: dict[str, str]) -> Training:
        """Constructor: baut ein Training aus einer CSV-Zeile (wirft ValueError/KeyError)."""
        return cls(
            datum=date.fromisoformat(row["datum"].strip()),
            sportart=row["sportart"].strip().capitalize(),
            distanz_km=float(row["distanz_km"]),
            dauer_min=float(row["dauer_min"]),
            hoehenmeter=int(row.get("hoehenmeter") or 0),
            notiz=(row.get("notiz") or "").strip(),
        )

    def to_row(self) -> dict[str, str]:
        return {
            "datum": self.datum.isoformat(),
            "sportart": self.sportart,
            "distanz_km": f"{self.distanz_km:g}",
            "dauer_min": f"{self.dauer_min:g}",
            "hoehenmeter": str(self.hoehenmeter),
            "notiz": self.notiz,
        }

    def with_note(self, notiz: str) -> Training:
        """Gibt eine Kopie mit neuer Notiz zurueck – das Original bleibt unveraendert."""
        return replace(self, notiz=notiz)


# --- Pure functions: gleicher Input -> gleicher Output, keine Seiteneffekte ---

def pace_min_pro_km(t: Training) -> float:
    if t.distanz_km <= 0:
        raise ValueError("Distanz muss groesser als 0 sein")
    return t.dauer_min / t.distanz_km


def geschwindigkeit_kmh(t: Training) -> float:
    if t.dauer_min <= 0:
        raise ValueError("Dauer muss groesser als 0 sein")
    return t.distanz_km / (t.dauer_min / 60)


def format_pace(minuten: float) -> str:
    """5.5 -> '5:30 min/km'"""
    sekunden = round(minuten * 60)
    return f"{sekunden // 60}:{sekunden % 60:02d} min/km"
