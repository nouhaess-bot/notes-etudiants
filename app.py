
import os
import sqlite3
from flask import Flask, jsonify, request
from auth import utilisateur_connecte

app = Flask(__name__)
DB = "notes.db"


def init_db():
    with sqlite3.connect(DB) as con:
        con.execute(
            "CREATE TABLE IF NOT EXISTS notes "
            "(id INTEGER PRIMARY KEY, etudiant TEXT, module TEXT, note REAL)"
        )
        if con.execute("SELECT COUNT(*) FROM notes").fetchone()[0] == 0:
            con.executemany(
                "INSERT INTO notes (etudiant, module, note) VALUES (?, ?, ?)",
                [
                    ("Amina", "DevSecOps", 15.5),
                    ("Youssef", "DevSecOps", 12.0),
                ],
            )


init_db()


@app.route("/")
def accueil():
    return """
    <html>
      <head><title>Consultation des notes</title></head>
      <body>
        <h1>Consultation des notes</h1>
        <a href="/notes">Voir les notes</a>
      </body>
    </html>
    """


@app.route("/health")
def health():
    return jsonify(status="ok")


@app.route("/notes", methods=["GET"])
def lister_notes():
    etudiant = request.args.get("etudiant", "")
    try:
        with sqlite3.connect(DB) as con:
            rows = con.execute(
                "SELECT id, etudiant, module, note FROM notes WHERE etudiant LIKE ?",
                (f"%{etudiant}%",),
            ).fetchall()
        return jsonify([
            {"id": r[0], "etudiant": r[1], "module": r[2], "note": r[3]}
            for r in rows
        ])
    except sqlite3.Error:
        return jsonify(erreur="Une erreur interne est survenue."), 500


@app.route("/notes/<int:note_id>", methods=["PUT"])
def modifier_note(note_id):
    utilisateur = utilisateur_connecte()

    if utilisateur is None:
        return jsonify(erreur="Authentification requise."), 401

    if utilisateur.get("role") != "enseignant":
        return jsonify(erreur="Action interdite."), 403

    donnees = request.get_json(silent=True)
    if not isinstance(donnees, dict) or "note" not in donnees:
        return jsonify(erreur="Note invalide."), 400

    note = donnees["note"]
    if isinstance(note, bool) or not isinstance(note, (int, float)):
        return jsonify(erreur="Note invalide."), 400

    if not 0 <= note <= 20:
        return jsonify(erreur="Note invalide."), 400

    try:
        with sqlite3.connect(DB) as con:
            resultat = con.execute(
                "SELECT module FROM notes WHERE id = ?", (note_id,)
            ).fetchone()

            if resultat is None:
                return jsonify(erreur="Note introuvable."), 404

            if resultat[0] != utilisateur.get("module"):
                return jsonify(erreur="Action interdite."), 403

            con.execute(
                "UPDATE notes SET note = ? WHERE id = ?",
                (note, note_id),
            )

        return jsonify(message="Note modifiée avec succès."), 200

    except sqlite3.Error:
        return jsonify(erreur="Une erreur interne est survenue."), 500


if __name__ == "__main__":
    app.run(host=os.environ.get("APP_HOST", "127.0.0.1"), port=5000)
