from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import sqlite3
import os
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
CORS(app) 


# Initialize Prometheus metrics
metrics = PrometheusMetrics(app)

# Database setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'todo.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Create tables if they don't exist
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

# Routes
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200

@app.route('/todos', methods=['GET'])
def get_todos():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT tid, task FROM tasks")
        tasks = [{'id': row[0], 'task': row[1]} for row in cursor.fetchall()]
    return jsonify(tasks)

@app.route('/todos', methods=['POST'])
def add_todo():
    data = request.json
    task = data.get('task')
    if not task:
        return jsonify({'error': 'Task is required'}), 400

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (task) VALUES (?)", (task,))
        conn.commit()
    return jsonify({'task': task}), 201

@app.route('/todos/<int:task_id>', methods=['DELETE'])
def delete_todo(task_id):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE tid=?", (task_id,))
        conn.commit()
    return '', 204

@app.route('/todos/<int:task_id>/done', methods=['POST'])
def move_to_done(task_id):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT task FROM tasks WHERE tid=?", (task_id,))
        task = cursor.fetchone()
        if task:
            cursor.execute("INSERT INTO done (task, task_id) VALUES (?, ?)", (task[0], task_id))
            cursor.execute("DELETE FROM tasks WHERE tid=?", (task_id,))
            conn.commit()
            return jsonify({'message': 'Moved to done'}), 200
        return jsonify({'error': 'Task not found'}), 404

@app.route('/done', methods=['GET'])
def get_done_tasks():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT did, task FROM done")
        done_tasks = [{'id': row[0], 'task': row[1]} for row in cursor.fetchall()]
    return jsonify(done_tasks)

@app.route('/done/<int:done_id>', methods=['DELETE'])
def delete_done_task(done_id):
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM done WHERE did=?", (done_id,))
        conn.commit()
    return '', 204


@app.route('/')
def home():
    return render_template('index.html')  # Serve the HTML frontend

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)