from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os

app = Flask(__name__)
app.secret_key = "change-this-secret-key"

DATABASE = "database.db"

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT NOT NULL,
            dob TEXT NOT NULL,
            gender TEXT NOT NULL,
            course TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

@app.route("/")
def index():
    return redirect(url_for("register"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        dob = request.form.get("dob", "").strip()
        gender = request.form.get("gender", "").strip()
        course = request.form.get("course", "").strip()
        password = request.form.get("password", "")

        if not all([name, email, phone, dob, gender, course, password]):
            flash("Please fill in all fields.", "error")
            return render_template("register.html")

        if len(password) < 6:
            flash("Password must contain at least 6 characters.", "error")
            return render_template("register.html")

        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO students
                (name, email, phone, dob, gender, course, password)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (name, email, phone, dob, gender, course, password))
            conn.commit()
            conn.close()
            return render_template("success.html", name=name, email=email)
        except sqlite3.IntegrityError:
            if 'conn' in locals():
                conn.close()
            flash("This email is already registered.", "error")
            return render_template("register.html")

    return render_template("register.html")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
