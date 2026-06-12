Welcome to **Chapter 5**! Right now, our app is a one-way street: it pulls data *out* of the database and shows it to the user, but the only way to add data is through the backend admin panel.

In this chapter, we turn it into a two-way street using **Django Forms**. We will allow users to submit new tasks directly from the home page safely and securely.

---

## Chapter 5: Forms and Validations

### The Big Concept: CSRF & ModelForms

When handling user input, web apps face two major issues: **security** and **data validation**.

* **Security (CSRF):** Hackers can trick users into submitting fake form requests. Django stops this using a **CSRF (Cross-Site Request Forgery) Token**—a unique secret key injected into every form that proves the submission came from *your* actual website.
* **ModelForms:** Instead of manually building an HTML form and mapping every text box to a database column, Django has a cheat code called `ModelForm`. You point Django to your database model, and it autogenerates the form fields, labels, and validation rules for you.

---

### Step 1: Create a Forms Blueprint

Inside your **`pages`** app folder, create a brand new file named **`forms.py`**.

Add this code to define a form based on our `Task` model from Chapter 3:

```python
# pages/forms.py
from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description'] # We only want the user to type these two
```

*(Notice we excluded `is_completed` and `created_at` because new tasks should default to pending and track time automatically).*

---

### Step 2: Update the View to Process Data

A single view function will now handle two different scenarios:

1. **GET Request:** The user just loaded the page. Show them an empty form.
2. **POST Request:** The user clicked "Submit". Grab their data, check if it's valid, save it to the database, and refresh the page.

Open **`pages/views.py`** and completely replace its contents with this updated logic:

```python
# pages/views.py
from django.shortcuts import render, redirect # Import redirect here
from .models import Task
from .forms import TaskForm # Import our new form

def home_page_view(request):
    # 1. If the user clicked the submit button (POST)
    if request.method == 'POST':
        form = TaskForm(request.POST) # Stuff the user's data into the form
        if form.is_valid(): # Django checks rules (e.g., max_length, required fields)
            form.save() # Automatically saves a new Task row to the database!
            return redirect('home') # Reload the page to clear the form
            
    # 2. If the user is just visiting the page normally (GET)
    else:
        form = TaskForm() # Create an empty, clean form

    # 3. Pull tasks to display on the page
    all_tasks = Task.objects.all().order_by('-created_at') # Newest tasks first
    
    context = {
        'task_list': all_tasks,
        'form': form # Pass the form to our HTML template
    }
    return render(request, 'home.html', context)
```

---

### Step 3: Embed the Form in the HTML Template

Open **`templates/home.html`** and add the HTML form right below your main title `<h1>`, but above the task list `<ul>`.

```html
<h1>🎯 My Central Task Hub</h1>
    <hr>

    <div style="background: #e9ecef; padding: 20px; margin-bottom: 30px; border-radius: 8px;">
        <h3>Add a New Task</h3>
        
        <form method="POST" action="">
            {% csrf_token %} 
            
            {{ form.as_p }} 
            
            <button type="submit" style="background-color: #007bff; color: white; padding: 10px 15px; border: none; border-radius: 4px; cursor: pointer;">
                Add Task
            </button>
        </form>
    </div>
    <ul>
```

---

### Step 4: Run it and Test Validation
Start your server if it isn't running:
```bash
python manage.py runserver
```

Go to `http://127.0.0.1:8000/`. You will see a clean input form.

* Try typing a task title and description, then hit **Add Task**. The page will reload instantly, and your new item will be sitting at the top of the task list!
* Try hitting **Add Task** without filling out the title field. Django will automatically stop the submission and yell at you to fill out the required field. That is built-in form validation at work!

---

Our application is now a functional mini-app where we can create and read data.