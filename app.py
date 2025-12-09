from flask import Flask, render_template, request, redirect, url_for
import threading
import webbrowser

app = Flask(__name__)

DAYS = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]

# Structure en mémoire : { "Lundi": [ {name, repetitions, weight, completed}, ... ], ... }
exercises = {day: [] for day in DAYS}


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", exercises=exercises)


@app.route("/add", methods=["POST"])
def add_exercise():
    name = request.form.get("name", "").strip()
    repetitions = request.form.get("repetitions", "").strip()
    weight = request.form.get("weight", "").strip()
    day = request.form.get("day", "Lundi")

    if day not in exercises:
        day = "Lundi"

    if not repetitions:
        repetitions = "0"
    if not weight:
        weight = "0"

    exercises[day].append({
        "name": name if name else "Sans nom",
        "repetitions": repetitions,
        "weight": weight,
        "completed": False
    })

    return redirect(url_for("index"))


@app.route("/complete/<day>/<int:index>", methods=["GET"])
def complete_exercise(day, index):
    try:
        if day in exercises and 0 <= index < len(exercises[day]):
            exercises[day][index]["completed"] = True
            return ("", 204)
        return ("Not found", 404)
    except Exception:
        return ("Error", 500)


@app.route("/cancel/<day>/<int:index>", methods=["POST"])
def cancel_exercise(day, index):
    try:
        if day in exercises and 0 <= index < len(exercises[day]):
            del exercises[day][index]
            return ("", 204)
        return ("Not found", 404)
    except Exception:
        return ("Error", 500)


@app.route("/reset/<day>/<int:index>", methods=["POST"])
def reset_exercise(day, index):
    try:
        if day in exercises and 0 <= index < len(exercises[day]):
            exercises[day][index]["completed"] = False
            return ("", 204)
        return ("Not found", 404)
    except Exception:
        return ("Error", 500)


def open_browser():
    webbrowser.open("http://127.0.0.1:5000")


if __name__ == "__main__":
    # Tu peux commenter l’ouverture auto du navigateur si tu veux
    # threading.Timer(1.0, open_browser).start()
    app.run(host="0.0.0.0", port=5000, debug=False)
