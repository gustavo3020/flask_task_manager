# Flask Task Manager

A simple yet robust web application for managing tasks, built with Flask and SQLAlchemy. This project demonstrates full CRUD (Create, Read, Update, Delete) operations, database integration, and basic web styling, serving as a foundational example of a Python-based web application.

---

## Features

* **Create Tasks:** Easily add new tasks with a description.
* **List Tasks:** View all existing tasks, along with their completion status and creation date.
* **Update Tasks:** Modify task descriptions and mark tasks as completed or incomplete.
* **Delete Tasks:** Remove tasks from the list.
* **Database Integration:** Persistent storage for tasks using SQLite and SQLAlchemy ORM.
* **Modular Structure:** Organized code with separate modules for application logic (`app.py`) and database models (`models.py`).
* **Basic Styling:** Simple CSS for an improved user interface.
* **Template Inheritance:** Efficient HTML structure using Jinja2's template inheritance (`base.html`).

---

## Technologies Used

* **Python 3.x**
* **Flask:** Web framework for building the application.
* **Flask-SQLAlchemy:** Flask extension for integrating SQLAlchemy (ORM) with Flask applications.
* **SQLite:** Lightweight, file-based relational database.
* **Jinja2:** Templating engine for rendering HTML.
* **HTML5:** Structure and content of web pages.
* **CSS3:** Styling and visual presentation.

---

## How to Run the Project

Follow these steps to set up and run the Flask Task Manager on your local machine.

### Prerequisites

* Python 3.x installed on your system.
* `pip` (Python package installer).

### 1. Clone the Repository (or navigate to your project folder)

If you're cloning:
```bash
git clone [https://github.com/gustavo3020/flask-task-manager.git](https://github.com/gustavo3020/flask-task-manager.git)
cd flask-task-manager
```
If you're already in your project folder, skip `git clone` and `cd`.

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
pip install Flask Flask-SQLAlchemy
```

### 5. Run the Application
Execute the app.py file to start the Flask development server.
```bash
python app.py
```

### 6. Access the Application
Open your web browser and navigate to:
```bash
http://127.0.0.1:5000/
```
You should see the Task Manager application running.

---

### Future Enhancements
* **User Authentication:** Implement user registration and login to allow individual task lists.
* **Form Validation:** Add more robust server-side form validation.
* **Flash Messages:** Provide user feedback with temporary success/error messages.
* **Improved UI/UX:** Enhance the user interface with a CSS framework (e.g., Tailwind CSS, Bootstrap).
* **Task Filtering/Sorting:** Add options to filter tasks by completion status or sort by date.