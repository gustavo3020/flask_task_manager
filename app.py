from flask import Flask, request, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, current_user, \
    login_required
from flask_migrate import Migrate
from models import db, Task, User
from sqlalchemy.exc import IntegrityError
from datetime import datetime
import os

# Create the Flask application and configure the secret key for sessions
app = Flask(__name__)
app.secret_key = 'b\x80V\xe1s\x00S\xdbd\xc2\xc9\x04\xf1\xf4\x8e\x16'

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
    'DATABASE_URL',
    'postgresql://postgres:x9abc4tv@localhost:5432/task_manager_db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database and Flask-Login
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

migrate = Migrate(app, db)


# User loader function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    """Loads a user from the database given their ID."""
    return User.query.get(int(user_id))


@app.route('/')
@login_required
def home():
    """
    Handles the main page, displaying tasks.

    This page is protected by the `@login_required` decorator, so only
    authenticated users can access it.

    This route fetches a list of tasks and renders the 'index.html' template.
    The tasks are initially filtered based on the current user's role, and
    can be further filtered using query parameters from the request, such as
    `completed`, `priority`, and `user_id`.

    Returns:
        Response: Renders 'index.html' with the filtered task list,
        the list of all users, and the `request.args` for persistent filters.
    """
    if current_user.role == 'master':
        query = Task.query
    else:
        # For non-master users, filter tasks by their role
        query = db.session.query(Task).join(User).filter(
            User.role == current_user.role
        )

    # Apply additional filters conditionally based on request arguments
    completed = request.args.get('completed')
    priority = request.args.get('priority')
    user_id = request.args.get('user_id')

    if completed == 'True':
        query = query.filter(Task.completed == True)
    elif completed == 'False':
        query = query.filter(Task.completed == False)

    if priority:
        try:
            query = query.filter(Task.priority == int(priority))
        except (ValueError, IndexError):
            flash('Invalid priority filter value.', 'error')

    if user_id:
        try:
            query = query.filter(Task.user_id == int(user_id))
        except (ValueError, IndexError):
            flash('Invalid user ID filter value.', 'error')

    tasks = query.all()
    users = User.query.all()

    # Pass the request arguments back to the template for sticky filters
    return render_template('index.html', tasks=tasks, users=users,
                           filter_args=request.args)


@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    """
    Handles the administration dashboard, displaying a list of all users.

    This route is protected to be accessible only by users with the 'master'
    role.
    It fetches all users from the database and passes them to the 'admin.html'
    template for display.

    Returns:
        Response: Renders 'admin.html' with a list of all users, or redirects
        to 'home' with an error if the user is not a 'master'.
    """
    if current_user.role != 'master':
        flash('You do not have permission to access this page.', 'error')
        return redirect(url_for('home'))

    return render_template('admin.html', users=User.query.all())


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Handles user login.

    If the user is already authenticated, it redirects them to the home page.
    On a POST request, it processes the login form, validates the user's
    credentials, and logs them in if successful.

    Returns:
        Response: Renders 'login.html' on GET or on failed login, or redirects
        to 'home' on successful login.
    """
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password.', 'error')

    return render_template('login.html')


@app.route('/logout', methods=['GET'])
def logout():
    """
    Handles user logout.

    This route logs the current user out and redirects them to the login page.
    """
    logout_user()
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    Handles user registration.

    On a GET request, it renders the 'register.html' template with the
    registration form.
    On a POST request, it processes the form submission to create a new user.
    It performs server-side validation to check for empty fields and duplicate
    emails.
    If registration is successful, it commits the new user to the database and
    redirects to the home page with a success message.
    If an error occurs, it flashes an appropriate message to the user.

    Returns:
        Response: Renders 'register.html' on GET or on form submission with
        errors, or redirects to 'home' on successful registration.
    """
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == 'POST':
        user_name = request.form.get('user_name')
        email = request.form.get('email')
        password = request.form.get('password')

        if not all([user_name, email, password]):
            flash('All fields are required.', 'error')
        else:
            try:
                new_user = User(user_name=user_name, email=email)
                new_user.set_password(password)
                db.session.add(new_user)
                db.session.commit()
                flash('Registration successful! Please log in to continue.',
                      'success')
                return redirect(url_for('login'))
            except IntegrityError:
                db.session.rollback()
                flash('''This email is already registered. Please use a
                      different one.''', 'error')
            except Exception as e:
                db.session.rollback()
                flash(f'An unexpected error occurred: {e}', 'error')

    return render_template('register.html')


@app.route('/task_detail/<int:task_id>')
@login_required
def task_detail(task_id):
    """
    Handles displaying the details of a single task.

    This page is protected by the `@login_required` decorator. All
    authenticated users have permission to view any task's details, regardless
    of who created it.

    Args:
        task_id (int): The unique identifier of the task to be displayed.

    The function fetches the task from the database using its ID. If the task
    is not found, a 404 error page is returned automatically.

    Returns:
        Response: Renders the 'task_detail.html' template, passing the
        requested task object.
    """
    task = db.get_or_404(Task, task_id)
    return render_template('task_detail.html', task=task)


@app.route('/create_task', methods=['GET', 'POST'])
@login_required
def create_task():
    """
    Handles the creation of a new task.

    This page is protected by the `@login_required` decorator, so only
    authenticated users can access it.

    On a GET request, it renders the 'create_task.html' template, which
    contains the form for adding a new task.

    On a POST request, it processes the form submission to create a new task
    with a title, description, priority, and due date. It validates the data
    types and, if successful, adds the new task to the database and
    redirects to the home page.

    Returns:
        Response: Renders 'create_task.html' on GET, or redirects to 'home'
        on POST.
    """
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        priority_str = request.form.get('priority')
        due_date_str = request.form.get('due_date')

        if title:
            try:
                priority = int(priority_str) if priority_str else 1
                due_date = datetime.strptime(
                    due_date_str, '%Y-%m-%d').date() if due_date_str else None

                new_task = Task(
                    title=title,
                    description=description,
                    priority=priority,
                    due_date=due_date,
                    user_id=current_user.id
                )
                db.session.add(new_task)
                db.session.commit()
            except (ValueError, IndexError):
                flash('Invalid data submitted for priority or due date.',
                      'error')

            return redirect(url_for('home'))

    return render_template('create_task.html')


@app.route('/update_task/<int:task_id>', methods=['GET', 'POST'])
@login_required
def update_task(task_id):
    """
    Handles updating an existing task based on its ID.

    This page is protected by the `@login_required` decorator, so only
    authenticated users can access it.

    Args:
        task_id (int): The unique identifier of the task to be updated.

    On a GET request, it renders the 'update_task.html' template, pre-filling
    the form with all the current task details, including title, description,
    priority, and due date.

    On a POST request, it processes the form submission to update the task's
    title, description, priority, due date, and completion status. After
    updating, it commits the changes to the database and redirects to the home
    page.

    A security check is performed to ensure only the task's author or a
    'master' user can perform the update.

    Returns:
        Response: Renders 'update_task.html' on GET, or redirects to 'home' on
        POST.
    """
    task = db.get_or_404(Task, task_id)
    if task.user_id != current_user.id and current_user.role != 'master':
        flash('You do not have permission to update this task.', 'error')
        return redirect(url_for('home'))

    if request.method == 'POST':
        task.title = request.form['title']
        task.description = request.form['description']
        task.priority = request.form['priority']
        task.due_date = request.form['due_date']
        task.completed = request.form.get('completed') == 'True'
        db.session.commit()
        return redirect(url_for('home'))

    return render_template('update_task.html', task=task)


@app.route('/delete_task/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    """
    Handles deleting an existing task based on its ID.

    This page is protected by the `@login_required` decorator, so only
    authenticated users can access it.

    Args:
        task_id (int): The unique identifier of the task to be deleted.

    On a POST request, it deletes the specified task from the database.
    After deletion, it commits the changes and redirects to the home page.

    Security check is performed to ensure only the task's author or a 'master'
    user can perform the deletion.

    Returns:
        Response: Redirects to the 'home' page.
    """
    task_to_delete = db.get_or_404(Task, task_id)

    if (task_to_delete.user_id != current_user.id
            and current_user.role != 'master'):
        flash('You do not have permission to delete this task.', 'error')
        return redirect(url_for('home'))

    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


@app.route('/update_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def update_user(user_id):
    """
    Handles updating an existing user's information, accessible only to
    'master' users.

    Args:
        user_id (int): The unique identifier of the user to be updated.

    On a GET request, it renders the 'update_user.html' template with the
    user's current information. On a POST request, it processes form data to
    update the user's name, email, and role.

    A security check is performed to prevent a 'master' user from accidentally
    updating their own role.

    Returns:
        Response: Renders 'update_user.html' on GET, or redirects to 'admin'
        on POST.
    """
    user = db.get_or_404(User, user_id)
    if current_user.role != 'master':
        flash('You do not have permission to update users.', 'error')
        return redirect(url_for('home'))

    if request.method == 'POST':
        if current_user.id == user.id:
            flash("You cannot update your own role.", "error")
            return redirect(url_for('admin'))

        user.user_name = request.form['user_name']
        user.email = request.form['email']
        user.role = request.form['role']
        db.session.commit()
        flash(f'User {user.user_name} updated successfully.', 'success')
        return redirect(url_for('admin'))

    return render_template('update_user.html', user=user)


@app.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    """
    Handles deleting an existing user, accessible only to 'master' users.

    Args:
        user_id (int): The unique identifier of the user to be deleted.

    On a POST request, it deletes the specified user from the database.

    A security check is performed to prevent a 'master' user from accidentally
    deleting their own account.

    Returns:
        Response: Redirects to the 'admin' page.
    """
    user_to_delete = db.get_or_404(User, user_id)

    if current_user.role != 'master':
        flash('You do not have permission to delete users.', 'error')
        return redirect(url_for('home'))

    if current_user.id == user_to_delete.id:
        flash("You cannot delete your own account.", "error")
        return redirect(url_for('admin'))

    db.session.delete(user_to_delete)
    db.session.commit()
    flash(f'User {user_to_delete.user_name} deleted successfully.', 'success')
    return redirect(url_for('admin'))


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False, host='0.0.0.0')
