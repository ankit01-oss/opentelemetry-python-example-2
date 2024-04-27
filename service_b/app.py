from flask import Flask, jsonify, request
from pymongo import MongoClient
from bson import ObjectId
from otel_setup import tracer  # Import the tracer

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client.todo_db  # Database
tasks_collection = db.tasks  # Collection for tasks

app = Flask(__name__)

# Endpoint to add a new task
@app.route("/add-task", methods=["POST"])
def add_task():
    task_data = request.json
    with tracer.start_as_current_span("service_b.add_task"):
        new_task = {
            "title": task_data.get("title"),
            "completed": False,
        }
    result = tasks_collection.insert_one(new_task)
    return jsonify({"_id": str(result.inserted_id), "message": "Task added"})

# Endpoint to get all tasks
@app.route("/get-tasks", methods=["GET"])
def get_tasks():
    with tracer.start_as_current_span("service_b.get_tasks"):
        tasks = list(tasks_collection.find())
    formatted_tasks = [
        {
            "_id": str(task["_id"]),
            "title": task["title"],
            "completed": task["completed"],
        }
        for task in tasks
    ]
    return jsonify(formatted_tasks)

# Endpoint to mark a task as completed
@app.route("/complete-task/<task_id>", methods=["PUT"])
def complete_task(task_id):
    with tracer.start_as_current_span("service_b.complete_task"):
        result = tasks_collection.update_one(
            {"_id": ObjectId(task_id)},
            {"$set": {"completed": True}}
        )
    if result.matched_count == 0:
        return jsonify({"error": "Task not found"}), 404
    return jsonify({"message": "Task marked as completed"})

if __name__ == "__main__":
    app.run(port=5001, debug=False, use_reloader=False)