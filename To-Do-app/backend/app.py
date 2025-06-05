from flask import Flask, jsonify, request
from flask_cors import CORS
from prometheus_flask_exporter import PrometheusMetrics
import sqlite3
import os
from contextlib import closing

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
metrics = PrometheusMetrics(app)
metrics.info('app_info', 'Todo Backend Application', version='1.0.0')

# Constants
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'todo.db')

# Database Helper Functions
def get_db_connection():
    """Returns a SQLite connection with Row factory."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database with tasks table."""
    with closing(get_db_connection()) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                tid INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT NOT NULL,
                done INTEGER NOT NULL DEFAULT 0 CHECK (done IN (0, 1))
        ''')
        conn.commit()

init_db()

# Helper: Validate JSON input
def validate_task_data(data):
    if not data or 'task' not in data:
        return False, jsonify({'error': 'Task field is required'}), 400
    return True, None

# Routes
@app.route('/')
def index():
    return jsonify({"message": "Todo Backend Service"})

@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy'}), 200

@app.route('/todos', methods=['GET'])
def get_todos():
    try:
        with closing(get_db_connection()) as conn:
            tasks = conn.execute("SELECT tid, task, done FROM tasks").fetchall()
        return jsonify([{
            'id': row['tid'],
            'task': row['task'],
            'done': bool(row['done'])
        } for row in tasks])
    except Exception as e:
        app.logger.error(f"Database error: {str(e)}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/todos', methods=['POST'])
def add_todo():
    data = request.get_json()
    is_valid, error_response = validate_task_data(data)
    if not is_valid:
        return error_response

    try:
        with closing(get_db_connection()) as conn:
            conn.execute("INSERT INTO tasks (task) VALUES (?)", (data['task'],))
            conn.commit()
        return jsonify({'message': 'Task added successfully'}), 201
    except Exception as e:
        app.logger.error(f"Failed to add task: {str(e)}")
        return jsonify({'error': 'Failed to add task'}), 500

@app.route('/todos/<int:task_id>/done', methods=['PUT'])
def toggle_done(task_id):
    data = request.get_json()
    if 'done' not in data or not isinstance(data['done'], bool):
        return jsonify({'error': 'Invalid or missing done field (must be boolean)'}), 400
    
    try:
        with closing(get_db_connection()) as conn:
            cursor = conn.execute(
                "UPDATE tasks SET done = ? WHERE tid = ?",
                (int(data['done']), task_id)
            )
            conn.commit()
            if cursor.rowcount == 0:
                return jsonify({'error': 'Task not found'}), 404
        return jsonify({'message': 'Task updated successfully'})
    except Exception as e:
        app.logger.error(f"Failed to update task: {str(e)}")
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/todos/<int:task_id>', methods=['DELETE'])
def delete_todo(task_id):
    try:
        with closing(get_db_connection()) as conn:
            cursor = conn.execute("DELETE FROM tasks WHERE tid = ?", (task_id,))
            conn.commit()
            if cursor.rowcount == 0:
                return jsonify({'error': 'Task not found'}), 404
        return jsonify({'message': 'Task deleted successfully'})
    except Exception as e:
        app.logger.error(f"Failed to delete task: {str(e)}")
        return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=os.getenv('FLASK_DEBUG', False))