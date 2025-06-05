from flask import Flask, jsonify, request
from flask_cors import CORS
from prometheus_flask_exporter import PrometheusMetrics
import sqlite3
import os

app = Flask(__name__)
CORS(app)
metrics = PrometheusMetrics(app)

# Database setup
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, 'todo.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

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

# Routes

@app.route('/')
def index():
    return jsonify({"message": "Backend is running"})

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
    data = request.get_json()
    task = data.get('task') if data else None
    if not task:
        return jsonify({'error': 'Task is required'}), 400

    with get_db_connection() as conn:
        conn.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
        conn.commit()
    return jsonify({'message': 'Task added successfully'}), 201

# You can add more routes for updating or deleting tasks if needed

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
