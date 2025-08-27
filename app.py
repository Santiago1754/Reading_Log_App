from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

# --- Initialize DB ---
def init_db():
    conn = sqlite3.connect("reading_log.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student TEXT NOT NULL,
                    book TEXT NOT NULL,
                    date TEXT NOT NULL,
                    summary TEXT
                )''')
    conn.commit()
    conn.close()

init_db()

# --- Student Page ---
@app.route("/", methods=["GET", "POST"])
def student():
    if request.method == "POST":
        student = request.form["student"]
        book = request.form["book"]
        summary = request.form["summary"]
        date = datetime.now().strftime("%Y-%m-%d")

        conn = sqlite3.connect("reading_log.db")
        c = conn.cursor()
        c.execute("INSERT INTO logs (student, book, date, summary) VALUES (?, ?, ?, ?)",
                  (student, book, date, summary))
        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("student.html")

# --- Teacher Dashboard ---
@app.route("/teacher")
def teacher():
    conn = sqlite3.connect("reading_log.db")
    c = conn.cursor()
    c.execute("SELECT student, book, date, summary FROM logs ORDER BY date DESC")
    logs = c.fetchall()
    conn.close()

    return render_template("teacher.html", logs=logs)

if __name__ == "__main__":
    app.run(debug=True)
