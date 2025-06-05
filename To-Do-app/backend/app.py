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
                task TEXT NOT NULL,
                done INTEGER NOT NULL DEFAULT 0
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
    try:
        with get_db_connection() as conn:
            tasks = conn.execute("SELECT tid, task, done FROM tasks").fetchall()
        return jsonify([{'id': row['tid'], 'task': row['task'], 'done': bool(row['done'])} for row in tasks])
    except Exception as e:
        print("Error fetching tasks:", e)
        return jsonify({'error': 'Internal Server Error'}), 500

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

@app.route('/todos/<int:task_id>/done', methods=['PUT'])
def toggle_done(task_id):
    data = request.get_json()
    done = data.get('done')
    if done is None:
        return jsonify({'error': 'Missing done field'}), 400
    with get_db_connection() as conn:
        cursor = conn.execute("UPDATE tasks SET done = ? WHERE tid = ?", (int(done), task_id))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({'error': 'Task not found'}), 404
    return jsonify({'message': 'Task updated successfully'})

@app.route('/todos/<int:task_id>', methods=['DELETE'])
def delete_todo(task_id):
    with get_db_connection() as conn:
        cursor = conn.execute("DELETE FROM tasks WHERE tid = ?", (task_id,))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({'error': 'Task not found'}), 404
    return jsonify({'message': 'Task deleted successfully'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
