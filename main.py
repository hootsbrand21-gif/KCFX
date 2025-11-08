from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_socketio import SocketIO, emit
from datetime import datetime
import pytz, random, json
from strategy import analyze_gold

app = Flask(__name__)
app.secret_key = "replace_this_with_a_random_key"
socketio = SocketIO(app, cors_allowed_origins="*")
LAGOS = pytz.timezone("Africa/Lagos")

users = {}       # simple in-memory demo store
signals = []     # simulated signal history

@app.route("/")
def home():
    if "user" in session:
        return redirect(url_for("dashboard"))
    return render_template("login.html")

@app.route("/signup", methods=["GET","POST"])
def signup():
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]
        users[u] = p
        return redirect(url_for("home"))
    return render_template("signup.html")

@app.route("/login", methods=["POST"])
def login():
    u = request.form["username"]; p = request.form["password"]
    if users.get(u) == p:
        session["user"] = u
        return redirect(url_for("dashboard"))
    return "Invalid login"

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("home"))
    return render_template("dashboard.html", user=session["user"], signals=signals)

@app.route("/analyze", methods=["POST"])
def analyze():
    data = analyze_gold()
    now = datetime.now(LAGOS).strftime("%Y-%m-%d %H:%M:%S")
    data["time"] = now
    signals.append(data)
    socketio.emit("kcf_signal", data)
    return jsonify(data)

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host="0.0.0.0", port=port)


