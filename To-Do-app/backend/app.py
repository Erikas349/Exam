from flask import Flask, jsonify, request
import boto3
import logging

cloudwatch = boto3.client('cloudwatch')
logging.basicConfig(filename='app.log', level=logging.INFO,)

app = Flask(__name__)

todos =[]

@app.route('/todos', methods=['GET'])
def get_todos():
    return jsonify(todos)

@app.route('/todos', methods=['POST'])
def add_todo():
    todo = request.json
    todos.append(todo)
    return jsonify(todo), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

app.config['sqlalchemy_database_uri'] = 'postgresql://user:password@todo-db.xyz.eu-central-1.rds.amazonaws.com/todo'

app.route('/health')
def health():
    return {'status': 'healthy'}, 200

@app.route('/metrics')
def metrics():
    cloudwatch.put_metric_data(
        Namespace='TodoApp',
        MetricData=[{'MetricName': 'Requests', 'Value': 1}]
        
    )