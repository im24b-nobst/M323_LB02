from pathlib import Path

from flask import Flask, render_template

from trainingslog.models import format_pace, pace_min_pro_km
from trainingslog.storage import lade_trainings

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


if __name__ == "__main__":
    app.run(debug=True)
