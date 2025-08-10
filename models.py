from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class User(db.Model, UserMixin):
    """
    Represents a user in the task manager application.

    This model stores user credentials and role, which are essential for
    authentication and managing task permissions.

    Attributes:
        id (int): Primary key, unique identifier for the user.
        user_name (str): The user's chosen name, used for login and display.
        email (str): The user's email address, must be unique.
        role (str): The user's access level or department (e.g., 'master').
        password_hash (str): A secure hash of the user's password.
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(50), nullable=False, default='common')
    password_hash = db.Column(db.String(200), nullable=False)
    tasks = db.relationship('Task', backref='author', lazy=True)

    def set_password(self, password):
        """Hashes the password and sets it to the password_hash attribute."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Checks if the provided password matches the stored hash."""
        return check_password_hash(self.password_hash, password)


class Task(db.Model):
    """
    Represents a single task in the task manager application.

    Attributes:
        id (int): Primary key, unique identifier for the task.
        title (str): The main title of the task.
        description (str): A detailed description of the task.
        priority (int): The priority level of the task (e.g., 1=Low, 5=High).
        due_date (datetime): The deadline for the task.
        completed (bool): Indicates whether the task is completed (True) or not
        (False).
        created_at (datetime): Timestamp when the task was created.
        user_id (int): Foreign key linking the task to the user who created it.
    """
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String)
    priority = db.Column(db.Integer, default=1)
    due_date = db.Column(db.Date)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.Date, default=db.func.current_date())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        """
        Returns a string representation of the Task object.
        """
        return f'<Task {self.id}: {self.title}>'
