Welcome to **Chapter 6**! Security isn't just an afterthought in Django; it's baked right into the core framework.

Right now, anyone who visits your website can see, add, and alter tasks. In this chapter, we lock down our application using **Django's Built-in Authentication System**. We will connect our tasks to specific users, build a secure login page, and ensure users can *only* see and manage their own private to-do list.

---

## Chapter 6: Authentication and Security

### The Big Concept: Relationships & Access Control

To make our application secure and user-specific, we need to accomplish two things:

1. **User-to-Data Relationship:** We must tell the database that each task belongs to a specific user. We do this using a **Foreign Key** (a many-to-one relationship, meaning one user can have many tasks).
2. **Access Control:** We need to block unauthenticated visitors from accessing the page and dynamically filter our database queries based on whoever is currently logged in.

---

### Step 1: Link Tasks to Users (Database Update)

Django comes pre-packaged with a robust `User` model that handles passwords, hashing, and permissions securely. Let's link our `Task` model to it.

Open **`pages/models.py`** and update it to look like this:

```python
# pages/models.py
from django.db import models
from django.contrib.auth.models import User # 👈 Import Django's built-in User model

class Task(models.Model):
    # 👈 Link each task to a specific user
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) 
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
```

> 💡 **What does `on_delete=models.CASCADE` mean?** This is a safety rule. It tells Django: "If a user deletes their account, automatically wipe out all of their associated tasks as well so no orphan data is left behind."

Because we modified our database model, we must perform our two-step migration dance in the terminal:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### Step 2: Enable Authentication Routes & Settings

Django has built-in views for handling logging in and out, but we need to tell our project where to route them and where to send users after they log in.

First, open **`core_project/urls.py`** and include the built-in authentication system URLs:

```python
# core_project/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')), # 👈 Adds login, logout, password resets
    path('', include('pages.urls')),
]
```

Next, scroll to the very bottom of **`core_project/settings.py`** and add these two routing commands:

```python
# core_project/settings.py

# Where to redirect the user after a successful login/logout
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = 'home'

```

---

### Step 3: Create the Login Interface

By default, Django's auth system expects a template located inside a folder path named `registration/login.html`.

1. Go to your root **`templates`** folder.
2. Inside it, create a new subfolder called **`registration`**.
3. Inside that `registration` folder, create a file named **`login.html`**.

Add this clean login layout to your new **`templates/registration/login.html`**:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Login</title>
</head>
<body style="font-family: Arial, sans-serif; margin: 100px auto; max-width: 400px; padding: 20px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); border-radius: 8px;">

    <h2>🔒 Access Secured Hub</h2>
    <hr>
    
    <form method="POST">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit" style="width: 100%; background-color: #28a745; color: white; padding: 10px; border: none; border-radius: 4px; cursor: pointer;">
            Login
        </button>
    </form>

</body>
</html>
```

---

### Step 4: Lock Down the Views and Filter the Data

Now we need to update our home page view logic so that:

1. Anonymous users are forced to go to the login page.
2. When a logged-in user saves a task, it automatically maps to *their* account.
3. Users only see *their own* data pool.

Open **`pages/views.py`** and update it with the `@login_required` decorator and filtering logic:

```python
# pages/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required # 👈 Import the gatekeeper decorator
from .models import Task
from .forms import TaskForm

@login_required # 👈 Forces users to log in before they can access this view function
def home_page_view(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            # Intercept the save process so we can attach the logged-in user
            task = form.save(commit=False)
            task.user = request.user # 👈 Tie the task to the current logged-in user
            task.save()
            return redirect('home')
    else:
        form = TaskForm()

    # 👈 CRITICAL: Filter tasks so users ONLY see their own items!
    all_tasks = Task.objects.filter(user=request.user).order_by('-created_at') 
    
    context = {
        'task_list': all_tasks,
        'form': form
    }
    return render(request, 'home.html', context)
```

---

### Step 5: Personalize the Dashboard Layout

Let’s add a personalized greeting and a secure logout feature to the top of our main interface. Open **`templates/home.html`** and insert this navbar-style wrapper right above your main title `<h1>`:

```html
<div style="display: flex; justify-content: space-between; align-items: center; background: #343a40; color: white; padding: 10px 20px; border-radius: 5px; margin-bottom: 20px;">
    <span>Welcome, <strong>{{ request.user.username }}</strong>!</span>
    
    <form method="POST" action="{% url 'logout' %}" style="margin: 0;">
        {% csrf_token %}
        <button type="submit" style="background: #dc3545; color: white; border: none; padding: 5px 10px; border-radius: 4px; cursor: pointer;">
            Logout
        </button>
    </form>
</div>
```

---

### Verify Your New Shielding Layer

Run your server: `python manage.py runserver` and head over to `http://127.0.0.1:8000/`.

1. Because of the gatekeeper decorator, Django will instantly block you and redirect you to `http://127.0.0.1:8000/accounts/login/`.
2. Log in using the **Superuser credentials** you generated in Chapter 3.
3. You will land safely back on the home page. Add a task like *"My Private Task"*.
4. Open an Incognito window or use a different browser, log in to the admin panel (`/admin`), and create a brand-new second user account. Log into the home page as this new user, and notice that the dashboard is completely blank for them! They cannot see the superuser's tasks.

---

You have built an isolated, authenticated, form-driven web pipeline!