from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

# Endpoint to add a new task
@app.route("/add-task", methods=["POST"])
def add_task():
    task_data = request.json
    response = requests.post("http://localhost:5001/add-task", json=task_data)
    return jsonify(response.json())

# Endpoint to get all tasks
@app.route("/get-tasks", methods=["GET"])
def get_tasks():
    response = requests.get("http://localhost:5001/get-tasks")
    return jsonify(response.json())

# Endpoint to mark a task as completed
@app.route("/complete-task/<task_id>", methods=["PUT"])
def complete_task(task_id):
    response = requests.put(f"http://localhost:5001/complete-task/{task_id}")
    return jsonify(response.json())

if __name__ == "__main__":
    app.run(port=5000, debug=False, use_reloader=False)