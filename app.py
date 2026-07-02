import sqlite3
from flask import Flask, render_template, redirect

app = Flask(__name__)


def create_database():

    conn = sqlite3.connect("team.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS team(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            role TEXT,
            available INTEGER
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM team")

    count = cursor.fetchone()[0]

    if count == 0:

        members = [

            ("Alex Rivers", "Senior Developer", 1),

            ("Samantha Chen", "UX Designer", 0),

            ("Jordan Taylor", "Project Manager", 1),

            ("Maria Garcia", "Marketing Lead", 0),

            ("David Wilson", "QA Engineer", 1)

        ]

        cursor.executemany(
            "INSERT INTO team(name,role,available) VALUES(?,?,?)",
            members
        )

    conn.commit()
    conn.close()


create_database()


@app.route("/")
def home():

    conn = sqlite3.connect("team.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM team")

    members = cursor.fetchall()

    conn.close()

    return render_template("index.html", members=members)


@app.route("/toggle/<int:id>")
def toggle(id):

    conn = sqlite3.connect("team.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT available FROM team WHERE id=?",
        (id,)
    )

    current = cursor.fetchone()[0]

    if current == 1:
        new_status = 0
    else:
        new_status = 1

    cursor.execute(
        "UPDATE team SET available=? WHERE id=?",
        (new_status, id)
    )

    conn.commit()
    conn.close()

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)