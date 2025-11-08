from flask import Blueprint, jsonify, request
from models import db, Task, User

task_bp = Blueprint("task_bp", __name__)

# -----------------------------
# CREATE TASK
# -----------------------------
@task_bp.route("/api/tasks", methods=["POST"])
def create_task():
    data = request.get_json()
    title = data.get("title")
    description = data.get("description")
    deadline = data.get("deadline")
    
    task = Task(title=title, description=description, deadline=deadline)
    db.session.add(task)
    db.session.commit()
    
    return jsonify({"message": "Task created", "task": task.to_dict()}), 201


# -----------------------------
# GET ALL TASKS
# -----------------------------
@task_bp.route("/api/tasks", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([t.to_dict() for t in tasks]), 200


# -----------------------------
# ASSIGN TASK TO USER
# -----------------------------
@task_bp.route("/api/tasks/assign", methods=["POST"])
def assign_task():
    data = request.get_json()
    task_id = data.get("task_id")
    user_id = data.get("user_id")

    task = Task.query.get(task_id)
    user = User.query.get(user_id)

    if not task or not user:
        return jsonify({"error": "Invalid task_id or user_id"}), 404

    task.assigned_to_user_id = user.id
    db.session.commit()

    return jsonify({
        "message": f"Task '{task.title}' assigned to {user.username}",
        "task": task.to_dict()
    }), 200


# -----------------------------
# GET TASKS FOR SPECIFIC USER
# -----------------------------
@task_bp.route("/api/tasks/user/<int:user_id>", methods=["GET"])
def get_user_tasks(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    tasks = Task.query.filter_by(assigned_to_user_id=user_id).all()
    return jsonify([t.to_dict() for t in tasks]), 200


# -----------------------------
# GET UNASSIGNED TASKS
# -----------------------------
@task_bp.route("/api/tasks/unassigned", methods=["GET"])
def get_unassigned_tasks():
    tasks = Task.query.filter_by(assigned_to_user_id=None).all()
    return jsonify([t.to_dict() for t in tasks]), 200


# -----------------------------
# GET ALL USERS
# -----------------------------
@task_bp.route("/api/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([u.to_dict() for u in users]), 200


# -----------------------------
# CREATE USER (simple)
# -----------------------------
@task_bp.route("/api/users", methods=["POST"])
def create_user():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    role = data.get("role", "Member")

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 400

    user = User(username=username, email=email, role=role)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User created", "user": user.to_dict()}), 201
