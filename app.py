from datetime import date
from pathlib import Path

from flask import Flask, render_template, request

from trainingslog.importer import import_csv, total_distanz
from trainingslog.models import SPORTARTEN, format_pace, pace_min_pro_km
from trainingslog.storage import lade_trainings, speichere_trainings

app = Flask(__name__)
app.config["DATA_FILE"] = Path(__file__).parent / "data" / "trainings.csv"


def datenpfad() -> Path:
    return app.config["DATA_FILE"]


@app.template_filter("pace")
def pace_filter(training) -> str:
    return format_pace(pace_min_pro_km(training))


@app.route("/")
def index():
    trainings = sorted(lade_trainings(datenpfad()), key=lambda t: t.datum, reverse=True)
    return render_template("index.html", trainings=trainings[:10], anzahl=len(trainings))


@app.route("/import", methods=["GET", "POST"])
def import_view():
    meldung = None
    if request.method == "POST":
        datei = request.files.get("datei")
        if not datei or not datei.filename:
            meldung = "Bitte eine CSV-Datei auswaehlen."
        else:
            trainings, verworfen = import_csv(datei.read().decode("utf-8-sig"))
            if trainings:
                speichere_trainings(datenpfad(), trainings)
                meldung = (f"{len(trainings)} Trainings ({total_distanz(trainings):.1f} km) "
                           f"importiert, {verworfen} Zeilen verworfen.")
            else:
                meldung = f"Keine gueltigen Trainings gefunden ({verworfen} Zeilen verworfen)."
    return render_template("import.html", meldung=meldung)


@app.route("/trainings")
def trainings_view():
    sportart = request.args.get("sportart", "")
    von = request.args.get("von", "")
    bis = request.args.get("bis", "")
    min_km = request.args.get("min_km", "")
    sortierung = request.args.get("sort", "datum")

    resultat = []
    for t in lade_trainings(datenpfad()):
        if sportart and t.sportart != sportart:
            continue
        if von and t.datum < date.fromisoformat(von):
            continue
        if bis and t.datum > date.fromisoformat(bis):
            continue
        if min_km and t.distanz_km < float(min_km):
            continue
        resultat.append(t)

    if sortierung == "distanz":
        resultat.sort(key=lambda t: t.distanz_km, reverse=True)
    else:
        resultat.sort(key=lambda t: t.datum, reverse=True)

    total_km = 0.0
    summe_pace = 0.0
    for t in resultat:
        total_km += t.distanz_km
        summe_pace += pace_min_pro_km(t)
    if len(resultat) > 0:
        durchschnitt_pace = format_pace(summe_pace / len(resultat))
    else:
        durchschnitt_pace = "-"

    return render_template("trainings.html", trainings=resultat, total_km=total_km,
                           durchschnitt_pace=durchschnitt_pace, sportarten=SPORTARTEN,
                           args=request.args)


if __name__ == "__main__":
    app.run(debug=True)
