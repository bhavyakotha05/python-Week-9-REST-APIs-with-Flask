from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

from app import db
from app.models import Task
from app.tasks.schemas import validate_task_data


class TaskListResource(Resource):
    """
    GET  /api/tasks  -> List tasks (pagination, filtering, sorting)
    POST /api/tasks  -> Create new task
    """

    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()

        # Query params
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 10, type=int)
        status = request.args.get("status")
        priority = request.args.get("priority")
        sort_by = request.args.get("sort_by", "created_at")
        sort_order = request.args.get("sort_order", "desc")

        query = Task.query.filter_by(user_id=user_id)

        # Filters
        if status:
            query = query.filter_by(status=status)
        if priority:
            query = query.filter_by(priority=priority)

        # Sorting
        if hasattr(Task, sort_by):
            column = getattr(Task, sort_by)
            query = query.order_by(column.desc() if sort_order == "desc" else column.asc())

        # Pagination
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        tasks = [{
            "id": t.id,
            "title": t.title,
            "description": t.description,
            "status": t.status,
            "priority": t.priority,
            "due_date": t.due_date.isoformat() if t.due_date else None,
            "created_at": t.created_at.isoformat(),
            "updated_at": t.updated_at.isoformat()
        } for t in pagination.items]

        return {
            "status": "success",
            "data": {
                "tasks": tasks,
                "pagination": {
                    "page": pagination.page,
                    "per_page": pagination.per_page,
                    "total_pages": pagination.pages,
                    "total_items": pagination.total
                }
            }
        }, 200

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        data = request.get_json()

        if not data:
            return {"status": "error", "message": "No input data"}, 400

        validation = validate_task_data(data)
        if not validation["valid"]:
            return {"status": "error", "errors": validation["errors"]}, 400

        task = Task(
            title=data["title"],
            description=data.get("description", ""),
            status=data.get("status", "pending"),
            priority=data.get("priority", "medium"),
            due_date=datetime.strptime(data["due_date"], "%Y-%m-%d").date()
            if data.get("due_date") else None,
            user_id=user_id
        )

        db.session.add(task)
        db.session.commit()

        return {
            "status": "success",
            "data": {
                "message": "Task created successfully",
                "task_id": task.id
            }
        }, 201


class TaskResource(Resource):
    """
    GET    /api/tasks/<id>
    PUT    /api/tasks/<id>
    DELETE /api/tasks/<id>
    """

    @jwt_required()
    def get(self, task_id):
        user_id = get_jwt_identity()
        task = Task.query.filter_by(id=task_id, user_id=user_id).first()

        if not task:
            return {"status": "error", "message": "Task not found"}, 404

        return {
            "status": "success",
            "data": {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "status": task.status,
                "priority": task.priority,
                "due_date": task.due_date.isoformat() if task.due_date else None,
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat()
            }
        }, 200

    @jwt_required()
    def put(self, task_id):
        user_id = get_jwt_identity()
        data = request.get_json()

        task = Task.query.filter_by(id=task_id, user_id=user_id).first()
        if not task:
            return {"status": "error", "message": "Task not found"}, 404

        validation = validate_task_data(data, update=True)
        if not validation["valid"]:
            return {"status": "error", "errors": validation["errors"]}, 400

        if "title" in data:
            task.title = data["title"]
        if "description" in data:
            task.description = data["description"]
        if "status" in data:
            task.status = data["status"]
        if "priority" in data:
            task.priority = data["priority"]
        if "due_date" in data:
            task.due_date = datetime.strptime(data["due_date"], "%Y-%m-%d").date()

        db.session.commit()

        return {
            "status": "success",
            "message": "Task updated successfully"
        }, 200

    @jwt_required()
    def delete(self, task_id):
        user_id = get_jwt_identity()
        task = Task.query.filter_by(id=task_id, user_id=user_id).first()

        if not task:
            return {"status": "error", "message": "Task not found"}, 404

        db.session.delete(task)
        db.session.commit()

        return {
            "status": "success",
            "message": "Task deleted successfully"
        }, 204
