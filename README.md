# Flask Task Manager

---

![alt text](images/image1.png)
![alt text](images/image2.png)
![alt text](images/image3.png)
![alt text](images/image4.png)
![alt text](images/image5.png)

---

This is a robust and dynamic web-based task management application built with Flask. It has evolved from a basic CRUD example into a full-featured application with a complete authentication system and role-based access control.

---

## Key Features

* **User Authentication:** A secure system for user registration, login, and logout using **Flask-Login**. This ensures that only authenticated users can access the application's core features.
* **Role-Based Access Control (RBAC):** The application distinguishes between `master` users and regular users. `master` users have access to an administrative dashboard and enhanced permissions.
* **Task Management (CRUD):**
    * **Create:** Authenticated users can create new tasks with details like title, description, priority, and due date.
    * **View:** The home page displays a list of tasks, which can be dynamically filtered by status, priority, or task owner.
    * **Update:** Users can edit the details of their own tasks.
    * **Delete:** Users can delete their own tasks.
* **User Management (Admin-only):**
    * The `master` role can view, update, and delete other user accounts from a dedicated admin dashboard.
    * Security checks are in place to prevent a `master` from accidentally altering their own role or deleting their own account.
* **Dynamic Filters:** The home page features a powerful filtering system, allowing users to narrow down the task list by multiple criteria using URL query parameters.
* **Database Integration:** Persistent storage for tasks using PostgreSQL and SQLAlchemy ORM.
* **Modular Structure:** Organized code with separate modules for application logic (`app.py`) and database models (`models.py`).
* **Basic Styling:** Simple CSS for an improved user interface.
* **Template Inheritance:** Efficient HTML structure using Jinja2's template inheritance (`base.html`).

---

## Technologies Used

* **Backend:** Python, Flask.
* **Database: PostgreSQL** (managed with **SQLAlchemy** and **Flask-Migrate**).
* **Authentication: Flask-Login** for session management.
* **Front-end:** HTML5, CSS3.
* **Templating:** Jinja2.

---

## How to Run the Project

Follow these steps to set up and run the application in your local environment.

### Prerequisites

* Python 3.x installed on your system.
* A running PostgreSQL database instance.

### 1. Clone the Repository (or navigate to your project folder)

If you're cloning:
```bash
git clone https://github.com/gustavo3020/flask-task-manager.git
cd flask-task-manager
```

### 2. Create a Virtual Environment (Recommended)

It's good practice to use a virtual environment to manage dependencies.

```bash
python -m venv venv
```

### 3. Activate the Virtual Environment
* **On Windows:**
    ```bash
    .\venv\Scripts\activate
    ```
* **On macOS/Linux:**
    ```bash
    source venv/bin/activate
    ```

### 4. Install Dependencies
Install the required Python packages using pip.
```bash
pip install Flask Flask-SQLAlchemy Flask-Migrate psycopg2-binary Flask-Login
```

### 5. Configure the Database Environment Variable
Set up your `DATABASE_URL` environment variable. You can use a `.env` file for this.
```env
DATABASE_URL=postgresql://postgres:x9abc4tv@localhost:5432/task_manager_db
```

### 6. Initialize the Database and Run Migrations
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

### 7. Run the Application
Execute the app.py file to start the Flask development server.
```bash
python app.py
```

### 8. Access the Application
Open your web browser and navigate to:
```bash
http://127.0.0.1:5000/
```
You should see the Task Manager application running.

---

> **Note:** The `SECRET_KEY` is hardcoded in `app.py` for local development. For a production environment, it should be set as a separate environment variable.
