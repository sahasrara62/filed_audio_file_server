"""Extensions module. Each extension is initialized in the application factory located in application.py."""

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()
