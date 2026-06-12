Welcome to **Chapter 3**! Now that we can route users to different web pages, it's time to give our website a memory.

In this chapter, we explore the **Model** in Django's MVT architecture. Models are how Django communicates with databases.

---

## Chapter 3: Models and Databases

### The Big Concept: What is an ORM?

Normally, to talk to a database, you have to write complex SQL (Structured Query Language) queries. Django uses an **ORM (Object-Relational Mapper)**.

The ORM is a translator: it allows you to write standard Python code (classes and objects), and it automatically converts that code into SQL tables and rows behind the scenes.

---

### Step 1: Meet the Default Database

Open `core_project/settings.py` and scroll down to the `DATABASES` section. You will see this:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

Out of the box, Django sets up **SQLite**. It’s a lightweight database that saves your data into a single file inside your project directory (`db.sqlite3`). No installation or configuration required!

---

### Step 2: Define Your Data Structure (The Model)

Let’s build a simple **Todo List** capability into our project. We need a table to store our tasks.

Open **`pages/models.py`** and add the following Python class:

```python
# pages/models.py
from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=200) # A short text field
    description = models.TextField(blank=True) # A long text field, optional
    is_completed = models.BooleanField(default=False) # A true/false checkbox
    created_at = models.DateTimeField(auto_now_add=True) # Automatically set timestamps

    def __str__(self):
        return self.title
```

> 💡 **What is `__str__` doing?** This function tells Django how to display this object in human-readable text. Instead of showing `<Task: Task object (1)>`, it will show the actual title of the task (e.g., `"Buy groceries"`).

---

### Step 3: Migrations (The Two-Step Dance)

Whenever you create or modify a model, you have to tell your database to update its blueprints. This is done via **migrations**.

Run these **two commands** in your terminal every time you change your database structure:

#### Part A: Draft the Blueprint

```bash
python manage.py makemigrations

```

*What this does:* Django looks at your `models.py` file, notices you made a new `Task` model, and writes a blueprint file inside a folder called `migrations/`.

#### Part B: Build the Database Tables

```bash
python manage.py migrate

```

*What this does:* Django reads that blueprint and physically builds/modifies the actual tables inside your `db.sqlite3` file.

---

### Step 4: The Django Admin Panel (Magic!)

One of Django's absolute best features is its built-in admin dashboard. It gives you a visual interface to manage your database immediately.

First, we need to register our `Task` model so it shows up in the admin dashboard. Open **`pages/admin.py`** and update it:

```python
# pages/admin.py
from django.contrib import admin
from .models import Task

admin.site.register(Task)
```

Next, you need to create a "Superuser" (an admin account) to log in. Run this command and follow the prompts (type a username, email, and password):

```bash
python manage.py createsuperuser
```

*(Note: When typing your password, the terminal will look blank for security. Just type it out and hit Enter.)*

---

### Step 5: See It In Action

Start your server up again:

```bash
python manage.py runserver
```

Now open your browser and go to: `http://127.0.0.1:8000/admin/`

Log in with the superuser credentials you just made. You will see a beautiful dashboard, and under the `PAGES` section, you'll see **Tasks**. Click **+ Add**, create a few dummy tasks, and hit save!

---

You now have a real database hooked up, and you’ve successfully stored information inside it using Python.