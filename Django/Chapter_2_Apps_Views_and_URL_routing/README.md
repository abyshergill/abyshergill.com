Awesome! Let’s dive straight into **Chapter 2**.

In this chapter, we are going to build the actual gears of your website. By the end of this layout, you will understand how Django takes a web request from a user, processes it, and spits back a response.

---

## Chapter 2: Apps, Views, and URL Routing

### The Big Concept: Project vs. App

Before writing code, you need to understand Django's philosophy on organization:

* **The Project:** The entire website (e.g., Amazon).
* **The App:** A self-contained module that does *one specific thing* (e.g., Amazon's cart system, Amazon's user review system).

A Django project is just a collection of various apps working together. This makes your code modular and reusable.

---

### Step 1: Create Your First App

Make sure your virtual environment is still active `(venv)`. Inside your main folder (where `manage.py` lives), run this command to create an app called `pages`:

```bash
python manage.py startapp pages
```

Look at your folder structure now. You have a new `pages` directory! Inside it, the most important files for now are:

* `views.py`: Where we write the logic for what happens when someone visits a page.
* `models.py`: Where we will define our database structure (in Chapter 3).

### Step 2: Register Your App

Django is strict. Just because you created the app doesn't mean Django knows it exists. We have to introduce them.

Open `core_project/settings.py`, scroll down to the `INSTALLED_APPS` list, and add `'pages',` at the bottom:

```python
# core_project/settings.py

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Custom Apps
    'pages', 
]
```

> ⚠️ **Common Gotcha:** Don't forget that comma at the end of `'pages',`! Python lists require proper separation.

---

### Step 3: Create Your First View

A "view" is just a Python function that takes a web request and returns a web response.

Open `pages/views.py` and delete whatever is there. Write a simple function that says hello:

```python
# pages/views.py
from django.http import HttpResponse

def home_page_view(request):
    return HttpResponse("<h1>Hello, World! This is my first Django view.</h1>")
```

---

### Step 4: Hook Up the URLs (Routing)

Right now, we have a view, but Django doesn't know *when* to fire it. We need to map a URL (like `www.yoursite.com/`) to this specific function.

The cleanest way to handle URLs in Django is to let each app handle its own routing, and then point the main project to that app.

First, create a brand new file inside your **`pages`** folder and name it **`urls.py`**.

Add the following code to `pages/urls.py`:

```python
# pages/urls.py
from django.urls import path
from .views import home_page_view

urlpatterns = [
    path('', home_page_view, name='home'), # '' means the root / home page
]
```

Finally, we need to tell the main project (`core_project`) to look at our `pages` app URLs. Open **`core_project/urls.py`** and modify it to look like this:

```python
# core_project/urls.py
from django.contrib import admin
from django.urls import path, include # Import include here

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pages.urls')), # This links our pages app URLs to the main site
]
```

---

### Step 5: Test Your Masterpiece!

Go back to your terminal and start up your server again:

```bash
python manage.py runserver
```

Now, open your browser and go to `http://127.0.0.1:8000/`. Instead of the old rocket ship, you should see your custom message boldly on the screen: **"Hello, World! This is my first Django view."**

---

### Challenge Checkpoint

To make sure you've grasped routing, try adding a second page by yourself right now:

1. Create a new view function in `pages/views.py` called `about_page_view` that returns text like `"About Me Page"`.
2. Add a new path in `pages/urls.py` so that when a user goes to `http://127.0.0.1:8000/about/`, it triggers your new view.
