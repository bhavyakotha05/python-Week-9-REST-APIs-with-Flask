from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.models import User
from app.users.schemas import serialize_user


class UserProfileResource(Resource):
    """
    GET /api/users/me
    Returns current logged-in user's profile
    """

    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)

        if not user:
            return {
                "status": "error",
                "message": "User not found"
            }, 404

        return {
            "status": "success",
            "data": serialize_user(user)
        }, 200


class UserListResource(Resource):
    """
    GET /api/users
    Returns all users (admin-style endpoint)
    """

    @jwt_required()
    def get(self):
        users = User.query.all()

        return {
            "status": "success",
            "data": [serialize_user(u) for u in users]
        }, 200
