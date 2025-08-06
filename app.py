from flask import Flask, request, render_template, redirect, url_for
from models import db, Task

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


@app.route('/', methods=['GET', 'POST'])
def home():
    """
    Handles the main page, displaying all tasks and allowing new task creation.

    GET: Renders the 'template.html' with a list of all existing tasks.
    POST: Processes the form submission to create a new task.
          If 'description' is provided, a new Task is added to the database.
          Redirects to the home page after creation.

    Returns:
        Response: Renders 'template.html' on GET, or redirects to 'home' on
        POST.
    """
    if request.method == 'POST':
        description = request.form.get('description')
        if description:
            new_task = Task(description=description)
            db.session.add(new_task)
            db.session.commit()
            return redirect(url_for('home'))

    tasks = Task.query.all()
    return render_template('index.html', tasks=tasks)


@app.route('/update_task/<int:task_id>', methods=['GET', 'POST'])
def update_task(task_id):
    """
    Handles updating an existing task based on its ID.

    Args:
        task_id (int): The unique identifier of the task to be updated.

    GET: Renders the 'update_task.html' template, pre-filling the form
         with the current task details.
    POST: Processes the form submission to update the task's description
          and completion status. Commits changes to the database.
          Redirects to the home page after update.

    Returns:
        Response: Renders 'update_task.html' on GET, or redirects to 'home' on
        POST.
    """
    task = db.get_or_404(Task, task_id)

    if request.method == 'POST':
        task.description = request.form['description']
        task.completed = 'completed' in request.form
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('update_task.html', task=task)


@app.route('/delete_task/<int:task_id>', methods=['POST'])
def delete_task(task_id):
    """
    Handles deleting an existing task based on its ID.

    Args:
        task_id (int): The unique identifier of the task to be deleted.

    POST: Deletes the specified task from the database.
          Redirects to the home page after deletion.

    Returns:
        Response: Redirects to the 'home' page.
    """
    task_to_delete = db.get_or_404(Task, task_id)
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True, use_reloader=False)
