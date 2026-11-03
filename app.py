import os
import sqlite3
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session, flash, abort
from werkzeug.security import check_password_hash

APP_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(APP_DIR, "expedicion_roma.db")

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY")
ADMIN_PASSWORD_HASH = os.environ.get("ADMIN_PASSWORD_HASH")

if not app.secret_key or not ADMIN_PASSWORD_HASH:
    raise RuntimeError(
        "Faltan FLASK_SECRET_KEY o ADMIN_PASSWORD_HASH. "
        "Sigue las instrucciones del archivo README.md."
    )

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS registrations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                group_name TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                paid INTEGER NOT NULL DEFAULT 0,
                reports INTEGER NOT NULL DEFAULT 0,
                admin_note TEXT NOT NULL DEFAULT ''
            )
        """)

def admin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("admin"):
            return redirect(url_for("admin_login"))
        return view(*args, **kwargs)
    return wrapped

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        group_name = request.form.get("group_name", "").strip()
        if not name or not group_name:
            flash("Completa tu nombre y tu curso o grupo.", "error")
        elif len(name) > 80 or len(group_name) > 40:
            flash("Comprueba la longitud de los datos introducidos.", "error")
        else:
            with get_db() as conn:
                conn.execute(
                    "INSERT INTO registrations (name, group_name) VALUES (?, ?)",
                    (name, group_name)
                )
            flash("¡Inscripción enviada correctamente! Gracias.", "success")
            return redirect(url_for("home"))
    return render_template("home.html")

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        if check_password_hash(ADMIN_PASSWORD_HASH, request.form.get("password", "")):
            session.clear()
            session["admin"] = True
            return redirect(url_for("admin_dashboard"))
        flash("La contraseña no es correcta.", "error")
    return render_template("login.html")

@app.route("/admin/logout")
@admin_required
def admin_logout():
    session.clear()
    return redirect(url_for("home"))

@app.route("/admin")
@admin_required
def admin_dashboard():
    with get_db() as conn:
        rows = conn.execute(
            "SELECT * FROM registrations ORDER BY created_at DESC, id DESC"
        ).fetchall()
    return render_template("admin.html", registrations=rows)

@app.route("/admin/update/<int:registration_id>", methods=["POST"])
@admin_required
def update_registration(registration_id):
    paid = 1 if request.form.get("paid") == "yes" else 0
    try:
        reports = int(request.form.get("reports", "0"))
        if not 0 <= reports <= 100:
            raise ValueError
    except ValueError:
        flash("El número de partes debe estar entre 0 y 100.", "error")
        return redirect(url_for("admin_dashboard"))
    note = request.form.get("admin_note", "").strip()[:500]
    with get_db() as conn:
        result = conn.execute(
            """UPDATE registrations
               SET paid=?, reports=?, admin_note=?
               WHERE id=?""",
            (paid, reports, note, registration_id)
        )
        if result.rowcount == 0:
            abort(404)
    flash("Inscripción actualizada.", "success")
    return redirect(url_for("admin_dashboard"))

@app.route("/admin/delete/<int:registration_id>", methods=["POST"])
@admin_required
def delete_registration(registration_id):
    with get_db() as conn:
        conn.execute("DELETE FROM registrations WHERE id=?", (registration_id,))
    flash("Inscripción eliminada.", "success")
    return redirect(url_for("admin_dashboard"))

init_db()

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
