from flask import Blueprint, request, jsonify
from models.task_model import Task
from views.task_view import render_task_list, render_task_detail
from functools import wraps
from utils.decorator import jwt_required, roles_required

task_bp = Blueprint("tasks", __name__)


@task_bp.route("/tasks", methods=["GET"])
@jwt_required
def get_tasks():
    tasks = Task.get_all()
    return jsonify(render_task_list(tasks)) 


@task_bp.route("/tasks/<int:id>", methods=["GET"])
@jwt_required
def get_task_by_id():
    task = Task.get_by_id(id)
    if not task:
        return jsonify({"error", "tarea no encontrada"}), 404
    return jsonify(render_task_detail(task))

@task_bp.route("/tasks", methods=["POST"])
@jwt_required
@roles_required("admin")
def create_task():
    data=request.json
    title = data.get("title")
    description = data.get("description")
    status = data.get("status")
    created_at = data.get("created_at")
    assigned_to = data.get("assigned_to")
    
    if title is None or description is None or status is None or created_at is None or assigned_to is None:
        return jsonify({"error", "faltan datos requeridos"}), 404
    
    print(title)
    print(description)
    print(status)
    print(created_at)
    print(assigned_to)
    
    task = Task(title=title, description=description, status=status, created_at=created_at, assigned_to=assigned_to)
    task.save()
    return jsonify(render_task_detail(task)),201

@task_bp.route("/tasks/<int:id>", methods=["PUT"])
@jwt_required
@roles_required("admin")
def update_task(id):
    
    task = Task.get_by_id(id)
    
    if not task:
        return jsonify({"error": "tarea no encontrada"}), 404
    
    data=request.json
    title = data.get("title")
    description = data.get("description")
    status = data.get("status")
    created_at = data.get("created_at")
    assigned_to = data.get("assigned_to")
    
    task.update(title, description, status, created_at, assigned_to)
    
    return jsonify(render_task_detail(task)), 200

@task_bp.route("/tasks/<int:id>", methods=["DELETE"])
@jwt_required
@roles_required("admin")
def delate_task(id):
    task = Task.get_by_id(id)
    
    if not task:
        return jsonify({"error": "Tarea no encontrada"}), 404

    task.delete()
  
    return "", 204

