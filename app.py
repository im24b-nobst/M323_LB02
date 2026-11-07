from pathlib import Path

from flask import Flask, render_template, request

from trainingslog.importer import import_csv, total_distanz
from trainingslog.models import format_pace, pace_min_pro_km
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


if __name__ == "__main__":
    app.run(debug=True)
