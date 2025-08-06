from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Task(db.Model):
    """
    Represents a single task in the task manager application.

    Attributes:
        id (int): Primary key, unique identifier for the task.
        description (str): A brief text describing the task.
        completed (bool): Indicates whether the task is completed (True) or not
        (False).
        created_at (datetime): Timestamp when the task was created.
    """
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        """
        Returns a string representation of the Task object.
        """
        return f'<Task {self.id}>'
