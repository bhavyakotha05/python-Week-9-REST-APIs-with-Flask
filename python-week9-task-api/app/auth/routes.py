from flask import request
from flask_restful import Resource
from flask_jwt_extended import create_access_token

from app import db
from app.models import User
from app.auth.utils import validate_registration_data


class RegisterResource(Resource):
    """
    POST /api/auth/register
    """

    def post(self):
        data = request.get_json()

        if not data:
            return {"status": "error", "message": "No input data"}, 400

        # validate
        errors = validate_registration_data(data)
        if errors:
            return {"status": "error", "errors": errors}, 400

        # check existing user
        if User.query.filter_by(email=data["email"]).first():
            return {
                "status": "error",
                "message": "Email already registered"
            }, 400

        if User.query.filter_by(username=data["username"]).first():
            return {
                "status": "error",
                "message": "Username already exists"
            }, 400

        # create user
        user = User(
            username=data["username"],
            email=data["email"]
        )
        user.set_password(data["password"])

        db.session.add(user)
        db.session.commit()

        # JWT token
        access_token = create_access_token(identity=user.id)

        return {
            "status": "success",
            "data": {
                "message": "User registered successfully",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email
                },
                "access_token": access_token
            }
        }, 201


class LoginResource(Resource):
    """
    POST /api/auth/login
    """

    def post(self):
        data = request.get_json()

        if not data:
            return {"status": "error", "message": "No input data"}, 400

        user = User.query.filter_by(email=data.get("email")).first()

        if not user or not user.check_password(data.get("password", "")):
            return {
                "status": "error",
                "message": "Invalid email or password"
            }, 401

        access_token = create_access_token(identity=user.id)

        return {
            "status": "success",
            "data": {
                "message": "Login successful",
                "access_token": access_token
            }
        }, 200
