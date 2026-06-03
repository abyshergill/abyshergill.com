Welcome to **Chapter 4**! Up until now, our web pages have been pretty ugly because we’ve been hardcoding raw HTML strings straight inside our Python views.

In this chapter, we explore the **Template** in Django's MVT architecture. We will separate our logic from our design, build beautiful HTML pages, and pull the tasks we saved in the database during Chapter 3 onto the screen dynamically.

---

## Chapter 4: Django Templates and Static Files

### The Big Concept: Django Template Language (DTL)

An ordinary HTML file is completely static—it can't run Python loops or display variables. Django fixes this by using **DTL (Django Template Language)**. DTL allows us to inject placeholders and logic tags directly into our HTML code.

Think of it as a blueprint where Django dynamically swaps out the placeholders with real data from your database right before serving the page to the user.

---

### Step 1: Tell Django Where to Look for HTML

While you can store templates inside your individual apps, it is a best practice to keep all your HTML files in one centralized folder at the root of your project.

1. In your root project folder (where `manage.py` lives), create a new directory called **`templates`**.
2. Inside that new `templates` folder, create a file named **`home.html`**.

Next, we have to tell Django to look into this new folder. Open **`core_project/settings.py`**, scroll to the `TEMPLATES` block, and update the `'DIRS'` list like this:

```python
# core_project/settings.py

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], # 👈 Add this line here!
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

---

### Step 2: Feed Database Data to the Template

Now, let’s rewrite our view so that it grabs our tasks from the database and hands them over to our new `home.html` file.

Open **`pages/views.py`** and change your home page function to use Django's `render` shortcut:

```python
# pages/views.py
from django.shortcuts import render
from .models import Task # Import our database model from Chapter 3

def home_page_view(request):
    # 1. Grab all tasks from the database
    all_tasks = Task.objects.all() 
    
    # 2. Package them into a Python dictionary called "context"
    context = {
        'task_list': all_tasks
    }
    
    # 3. Ship the context off to the HTML template
    return render(request, 'home.html', context)
```

---

### Step 3: Write the Dynamic HTML (DTL Syntax)

Open your empty **`templates/home.html`** file and add the following structure. Pay close attention to the curly braces `{}`—this is the magic of DTL.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>My Django Todo Hub</title>
</head>
<body style="font-family: Arial, sans-serif; margin: 40px; background-color: #f4f4f9;">

    <h1>🎯 My Central Task Hub</h1>
    <hr>

    <ul>
        {% for task in task_list %}
            <li style="background: white; padding: 15px; margin-bottom: 10px; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                
                <h3>{{ task.title }}</h3>
                <p>{{ task.description }}</p>
                
                {% if task.is_completed %}
                    <span style="color: green; font-weight: bold;">✅ Status: Completed</span>
                {% else %}
                    <span style="color: #d9534f; font-weight: bold;">⏳ Status: Pending</span>
                {% endif %}

            </li>
        {% empty %}
            <p>No tasks found! Log into the <a href="/admin">Admin Panel</a> to create some tasks.</p>
        {% endfor %}
    </ul>

</body>
</html>
```

### The Two Golden Rules of DTL:

* **`{{ variable }}` (Double Braces):** Used when you want to print out values onto the screen (like the task title).
* **`{% logic %}` (Brace-Percent):** Used for logic operations like loops, conditions, and template tags.

---

### Step 4: Fire Up the Server and Witness the Magic

Run your server again:

```bash
python manage.py runserver
```

Open your browser to `http://127.0.0.1:8000/`. You should now see an organized, styled display showing the actual tasks you typed into the admin portal during Chapter 3! Go ahead and add or edit tasks via the admin panel, refresh the home page, and watch it update dynamically.

---

You have officially connected all parts of the **MVT (Model-View-Template)** architecture!
