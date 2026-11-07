# Design-Blatt: Statistik-Seite

## 1. Ziel
Die Statistik-Seite zeigt auf einen Blick, wie viel ich trainiert habe und was meine Bestleistungen sind.

## 2. Deklarative Anforderungen (WAS, nicht WIE)
- Zeige die Kilometer pro Kalenderwoche.
- Zeige die Kilometer pro Sportart.
- Zeige pro Sportart das laengste und das schnellste Training (schnellstes erst ab 5 km).
- Zeige die 5 schnellsten Laeufe ab 5 km. Bei gleicher Pace kommt der laengere zuerst.
- Ohne Trainings zeigt die Seite "Keine Daten" statt eines Fehlers.

## 3. Datenfluss
```
CSV-Datei
  -> lade_trainings()     tuple[Training]
  -> km_pro_woche()       dict[Woche, km]
  -> km_pro_sportart()    dict[Sportart, km]
  -> bestleistungen()     dict[Sportart, {laengstes, schnellstes}]
  -> top_laeufe()         tuple[Training]
  -> statistik.html
```
Jede Funktion bekommt die Trainings und gibt einen neuen Wert zurueck. Nichts wird veraendert.

## 4. Datentypen
- `Training`: frozen dataclass (unveraenderlich)
- Rueckgaben als `tuple` und `dict`

## 5. Geplante Operatoren
| Funktion | Signatur | Operator |
|---|---|---|
| `km_pro_woche` | `Iterable[Training] -> dict[str, float]` | reduce |
| `km_pro_sportart` | `Iterable[Training] -> dict[str, float]` | reduce |
| `gruppiere_nach_sportart` | `Iterable[Training] -> dict[str, tuple]` | Gruppieren |
| `laengstes` | `tuple[Training] -> Training` | max mit key |
| `schnellstes` | `tuple[Training] -> Training or None` | filter + min mit key |
| `bestleistungen` | `Iterable[Training] -> dict` | Komposition der drei oberen |
| `top_laeufe` | `Iterable[Training], int -> tuple[Training]` | filter + sorted mit eigenem key |

## 6. Edge Cases
- keine Trainings -> leere Tabellen
- kein Training ab 5 km -> "schnellstes" ist leer
- gleiche Pace -> laengere Distanz zuerst
