import os
import sqlite3
from flask import Flask, g


def get_db():
    if "db" not in g:
        instance_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "instance")
        os.makedirs(instance_path, exist_ok=True)
        g.db = sqlite3.connect(os.path.join(instance_path, "app.db"), detect_types=sqlite3.PARSE_DECLTYPES)
        g.db.row_factory = sqlite3.Row
    return g.db


def init_db():
    db = get_db()
    cur = db.cursor()
    cur.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT,
            role TEXT DEFAULT 'user'
        );
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            author TEXT NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    cur.execute("SELECT COUNT(*) FROM users")
    if cur.fetchone()[0] == 0:
        cur.execute(
            "INSERT INTO users (username, password, email, role) VALUES (?, ?, ?, ?)",
            ("admin", "admin", "admin@vulnlab.local", "admin")
        )
        cur.execute(
            "INSERT INTO users (username, password, email, role) VALUES (?, ?, ?, ?)",
            ("user1", "password1", "user1@vulnlab.local", "user")
        )
        cur.execute(
            "INSERT INTO users (username, password, email, role) VALUES (?, ?, ?, ?)",
            ("user2", "password2", "user2@vulnlab.local", "user")
        )
    db.commit()


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "insecure-secret-for-pen-test-lab"
    app.config["DEBUG"] = True  # Intentional misconfiguration

    from app.routes import sqli_bp, xss_bp, auth_bp, idor_bp, path_traversal_bp
    from app.routes import cmd_injection_bp, csrf_bp, deserialize_bp, ssrf_bp, crypto_bp
    from app.routes import redirect_open_bp, xxe_bp, clickjacking_bp, misc_bp

    app.register_blueprint(sqli_bp, url_prefix="/sqli")
    app.register_blueprint(xss_bp, url_prefix="/xss")
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(idor_bp, url_prefix="/users")
    app.register_blueprint(path_traversal_bp, url_prefix="/file")
    app.register_blueprint(cmd_injection_bp, url_prefix="/cmd")
    app.register_blueprint(csrf_bp, url_prefix="/transfer")
    app.register_blueprint(deserialize_bp, url_prefix="/deserialize")
    app.register_blueprint(ssrf_bp, url_prefix="/ssrf")
    app.register_blueprint(crypto_bp, url_prefix="/crypto")
    app.register_blueprint(redirect_open_bp, url_prefix="/redirect")
    app.register_blueprint(xxe_bp, url_prefix="/xxe")
    app.register_blueprint(clickjacking_bp, url_prefix="/clickjacking")
    app.register_blueprint(misc_bp)

    @app.before_request
    def before_request():
        g.db = get_db()

    @app.teardown_appcontext
    def close_db(exception=None):
        db = g.pop("db", None)
        if db is not None:
            db.close()

    with app.app_context():
        init_db()

    return app
