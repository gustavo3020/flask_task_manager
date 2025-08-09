from flask import Flask, request, render_template, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, current_user, \
    login_required
from models import db, Task, User
from sqlalchemy.exc import IntegrityError

# Create the Flask application and configure the secret key for sessions
app = Flask(__name__)
app.secret_key = 'b\x80V\xe1s\x00S\xdbd\xc2\xc9\x04\xf1\xf4\x8e\x16'

# Database configuration (SQLite)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database and Flask-Login
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


# User loader function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    """Loads a user from the database given their ID."""
    return User.query.get(int(user_id))


@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
    """
    Handles the main page, displaying tasks and allowing new task creation.

    This page is protected by the `@login_required` decorator, so only
    authenticated users can access it.

    On a GET request, it renders the 'index.html' template with a list of
    tasks filtered by the current user's role.
    - 'master' users can see all tasks.
    - Other users can see tasks from all users who share their role.

    On a POST request, it processes the form submission to create a new task,
    associating it with the current user.

    Returns:
        Response: Renders 'index.html' on GET, or redirects to 'home' on POST.
    """
    if request.method == 'POST':
        description = request.form.get('description')
        if description:
            new_task = Task(description=description, user_id=current_user.id)
            db.session.add(new_task)
            db.session.commit()
            return redirect(url_for('home'))

    # Logic to filter tasks based on user role
    if current_user.role == 'master':
        tasks = Task.query.all()
    else:
        tasks = db.session.query(Task).join(User).filter(
            User.role == current_user.role).all()

    return render_template('index.html', tasks=tasks)


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
    the form with the current task details.
    On a POST request, it processes the form submission to update the task's
    description and completion status. After updating, it commits the changes
    to the database and redirects to the home page.

    Security check is performed to ensure only the task's author or a 'master'
    user can perform the update.

    Returns:
        Response: Renders 'update_task.html' on GET, or redirects to 'home' on
        POST.
    """
    task = db.get_or_404(Task, task_id)
    if task.user_id != current_user.id and current_user.role != 'master':
        flash('You do not have permission to update this task.', 'error')
        return redirect(url_for('home'))

    if request.method == 'POST':
        task.description = request.form['description']
        task.completed = 'completed' in request.form
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


if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True, use_reloader=False)
