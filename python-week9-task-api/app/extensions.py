from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_migrate import Migrate

# Database
db = SQLAlchemy()

# JWT Authentication
jwt = JWTManager()

# RESTful API
api = Api()

# Database migrations
migrate = Migrate()
