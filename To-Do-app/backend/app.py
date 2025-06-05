from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from prometheus_flask_exporter import PrometheusMetrics
import sqlite3
import os

app = Flask(__name__, template_folder='../templates', static_folder='../frontend/public')
CORS(app)
metrics = PrometheusMetrics(app)

# --- Database setup ---
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, 'todo.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Create tables on startup
def init_db():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                tid INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS done (
                did INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL,
                task_id INTEGER
            )
        ''')
        conn.commit()

init_db()

# --- API Routes ---

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

@app.route('/todos', methods=['GET'])
def get_todos():
    with get_db_connection() as conn:
        tasks = conn.execute("SELECT tid, task FROM tasks").fetchall()
    return jsonify([{'id': row['tid'], 'task': row['task']} for row in tasks])

@app.route('/todos', methods=['POST'])
def add_todo():
    data = request.get_jso_
