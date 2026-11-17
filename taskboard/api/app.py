import os

import psycopg
from flask import Flask, jsonify, request
from psycopg.rows import dict_row

app = Flask(__name__)


def read_password():
    """Lit le mot de passe depuis un fichier (secret) ou une variable."""
    path = os.environ.get("DB_PASSWORD_FILE")
    if path:
        with open(path) as f:
            return f.read().strip()
    return os.environ["DB_PASSWORD"]


def get_conn():
    return psycopg.connect(
        host=os.environ.get("DB_HOST", "db"),
        port=int(os.environ.get("DB_PORT", "5432")),
        dbname=os.environ["POSTGRES_DB"],
        user=os.environ["POSTGRES_USER"],
        password=read_password(),
        row_factory=dict_row,
        connect_timeout=3,
    )


@app.get("/api/health")
def health():
    try:
        with get_conn() as conn:
            conn.execute("SELECT 1")
        return jsonify(status="ok", host=os.uname().nodename)
    except Exception:
        app.logger.exception("health check failed")
        return jsonify(status="error"), 503


@app.get("/api/tasks")
def list_tasks():
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT id, title, done FROM tasks ORDER BY id"
        ).fetchall()
    return jsonify(rows)


@app.post("/api/tasks")
def create_task():
    data = request.get_json(silent=True) or {}
    title = (data.get("title") or "").strip()
    if not title:
        return jsonify(error="le champ 'title' est obligatoire"), 400
    with get_conn() as conn:
        row = conn.execute(
            "INSERT INTO tasks (title) VALUES (%s) RETURNING id, title, done",
            (title,),
        ).fetchone()
    return jsonify(row), 201
