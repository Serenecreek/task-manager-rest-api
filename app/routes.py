from flask import Blueprint, jsonify, request

from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required
)

from app.extensions import db
from app.models import Task, User


api = Blueprint("api", __name__)


# ============================================================
# HEALTH CHECK
# ============================================================

@api.route("/health", methods=["GET"])
def health_check():
    return jsonify({
        "status": "success",
        "message": "Task Manager API is running"
    }), 200


# ============================================================
# AUTHENTICATION
# ============================================================

@api.route("/auth/register", methods=["POST"])
def register():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({
            "error": "Username and password are required"
        }), 400

    username = username.strip()

    if not username:
        return jsonify({
            "error": "Username cannot be empty"
        }), 400

    if len(password) < 6:
        return jsonify({
            "error": "Password must be at least 6 characters"
        }), 400

    existing_user = User.query.filter_by(
        username=username
    ).first()

    if existing_user:
        return jsonify({
            "error": "Username already exists"
        }), 409

    user = User(username=username)

    # Never store the plain-text password.
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": "User registered successfully",
        "user": user.to_dict()
    }), 201


@api.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({
            "error": "Username and password are required"
        }), 400

    user = User.query.filter_by(
        username=username.strip()
    ).first()

    if not user or not user.check_password(password):
        return jsonify({
            "error": "Invalid username or password"
        }), 401

    # Store the user ID inside the JWT.
    access_token = create_access_token(
        identity=str(user.id)
    )

    return jsonify({
        "message": "Login successful",
        "access_token": access_token,
        "token_type": "Bearer"
    }), 200


@api.route("/auth/me", methods=["GET"])
@jwt_required()
def get_current_user():
    user_id = int(get_jwt_identity())

    user = db.session.get(User, user_id)

    if not user:
        return jsonify({
            "error": "User not found"
        }), 404

    return jsonify({
        "user": user.to_dict()
    }), 200


# ============================================================
# TASKS
# ============================================================

@api.route("/tasks", methods=["POST"])
@jwt_required()
def create_task():
    user_id = int(get_jwt_identity())

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    title = data.get("title")
    description = data.get("description", "")

    if not title:
        return jsonify({
            "error": "Title is required"
        }), 400

    title = title.strip()

    if not title:
        return jsonify({
            "error": "Title cannot be empty"
        }), 400

    if len(title) > 200:
        return jsonify({
            "error": "Title cannot exceed 200 characters"
        }), 400

    task = Task(
        title=title,
        description=description,
        user_id=user_id
    )

    db.session.add(task)
    db.session.commit()

    return jsonify({
        "message": "Task created successfully",
        "task": task.to_dict()
    }), 201


@api.route("/tasks", methods=["GET"])
@jwt_required()
def get_tasks():
    user_id = int(get_jwt_identity())

    tasks = Task.query.filter_by(
        user_id=user_id
    ).order_by(
        Task.created_at.desc()
    ).all()

    return jsonify({
        "count": len(tasks),
        "tasks": [
            task.to_dict()
            for task in tasks
        ]
    }), 200


@api.route("/tasks/<int:task_id>", methods=["GET"])
@jwt_required()
def get_task(task_id):
    user_id = int(get_jwt_identity())

    task = Task.query.filter_by(
        id=task_id,
        user_id=user_id
    ).first()

    if not task:
        return jsonify({
            "error": "Task not found"
        }), 404

    return jsonify({
        "task": task.to_dict()
    }), 200


@api.route("/tasks/<int:task_id>", methods=["PUT"])
@jwt_required()
def update_task(task_id):
    user_id = int(get_jwt_identity())

    task = Task.query.filter_by(
        id=task_id,
        user_id=user_id
    ).first()

    if not task:
        return jsonify({
            "error": "Task not found"
        }), 404

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    if "title" in data:
        title = data["title"]

        if not title or not title.strip():
            return jsonify({
                "error": "Title cannot be empty"
            }), 400

        if len(title.strip()) > 200:
            return jsonify({
                "error": "Title cannot exceed 200 characters"
            }), 400

        task.title = title.strip()

    if "description" in data:
        task.description = data["description"]

    if "completed" in data:
        if not isinstance(data["completed"], bool):
            return jsonify({
                "error": "Completed must be true or false"
            }), 400

        task.completed = data["completed"]

    db.session.commit()

    return jsonify({
        "message": "Task updated successfully",
        "task": task.to_dict()
    }), 200


@api.route("/tasks/<int:task_id>", methods=["DELETE"])
@jwt_required()
def delete_task(task_id):
    user_id = int(get_jwt_identity())

    task = Task.query.filter_by(
        id=task_id,
        user_id=user_id
    ).first()

    if not task:
        return jsonify({
            "error": "Task not found"
        }), 404

    db.session.delete(task)
    db.session.commit()

    return jsonify({
        "message": "Task deleted successfully"
    }), 200