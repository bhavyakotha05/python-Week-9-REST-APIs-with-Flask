from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_migrate import Migrate

# Extensions (global)
db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    # ======================
    # App Configuration
    # ======================
    app.config["SECRET_KEY"] = "dev-secret-key"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///task_api.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # JWT config
    app.config["JWT_SECRET_KEY"] = "jwt-secret-key"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 3600  # 1 hour

    # ======================
    # Initialize Extensions
    # ======================
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    # ======================
    # API setup
    # ======================
    api = Api(app)

    # ======================
    # Import Resources
    # (import here to avoid circular imports)
    # ======================
    from app.auth.routes import RegisterResource, LoginResource
    from app.tasks.routes import TaskListResource, TaskResource

    # ======================
    # Register Routes
    # ======================
    api.add_resource(RegisterResource, "/api/auth/register")
    api.add_resource(LoginResource, "/api/auth/login")

    api.add_resource(TaskListResource, "/api/tasks")
    api.add_resource(TaskResource, "/api/tasks/<int:task_id>")

    return app
