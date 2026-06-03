Welcome to **Chapter 7: The Capstone Project**! You have made it to the finish line. You've mastered routing, database models, migrations, dynamic templates, secure forms, and user authentication.

For your graduation project, we are going to build a fully functional, production-ready **DevTicket: A Collaborative Project Ticket Tracker**. This goes beyond a simple to-do list by implementing full **CRUD (Create, Read, Update, Delete)** capabilities, data relationships, status categories, and clean UI mechanics.

Let's build this entire application step by step.

---

## Chapter 7: Capstone Project – DevTicket Tracker

### Project Architecture Overview

Our Capstone project will consist of:

1. **Dashboard (Read All):** A secure dashboard showing user-specific project tickets categorized by priority.
2. **Ticket Detail (Read One):** A dedicated breakdown page for individual tickets.
3. **Ticket Creation (Create):** A form to log new project bugs or features.
4. **Ticket Modification (Update):** A pre-filled interface allowing owners to change descriptions, priorities, or completion statuses.
5. **Ticket Removal (Delete):** A safe confirmation state to wipe out data entries securely.

---

### Step 1: Initialize the Capstone App

Ensure your virtual environment is running (`venv`). In your terminal, generate a dedicated app for this project:

```bash
python manage.py startapp tickets
```

Register your new app immediately inside **`core_project/settings.py`**:

```python
# core_project/settings.py
INSTALLED_APPS = [
    # ... previous entries
    'pages',
    'tickets', # 👈 Add your capstone app here
]
```

---

### Step 2: Build a Multi-Field Database Model

We need our database entries to store various data types: text, choices (dropdowns), boolean toggles, and relational user keys.

Open **`tickets/models.py`** and implement this tracking model structure:

```python
# tickets/models.py
from django.db import models
from django.contrib.auth.models import User

class ProjectTicket(models.Model):
    # Setup choices for dropdown menus
    PRIORITY_CHOICES = [
        ('LOW', 'Low Priority'),
        ('MEDIUM', 'Medium Priority'),
        ('HIGH', 'High Priority'),
    ]
    
    STATUS_CHOICES = [
        ('BACKLOG', 'Backlog'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='LOW')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='BACKLOG')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"[{self.priority}] {self.title}"
```

Run your migrations in the terminal to prepare the database table:

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### Step 3: Construct the ModelForm with Frontend Styling

Let's construct a form that not only captures the input data but also injects clean styling classes directly into the HTML inputs via Django's `widgets`.

Open/create **`tickets/forms.py`**:

```python
# tickets/forms.py
from django import forms
from .models import ProjectTicket

class TicketForm(forms.ModelForm):
    class Meta:
        model = ProjectTicket
        fields = ['title', 'description', 'priority', 'status']
        
        # Adding HTML style styling definitions via widgets
        widgets = {
            'title': forms.TextInput(attrs={'style': 'width: 100%; padding: 8px; margin-top: 5px; border-radius: 4px; border: 1px solid #ccc;'}),
            'description': forms.Textarea(attrs={'rows': 4, 'style': 'width: 100%; padding: 8px; margin-top: 5px; border-radius: 4px; border: 1px solid #ccc;'}),
            'priority': forms.Select(attrs={'style': 'width: 100%; padding: 8px; margin-top: 5px; border-radius: 4px; border: 1px solid #ccc;'}),
            'status': forms.Select(attrs={'style': 'width: 100%; padding: 8px; margin-top: 5px; border-radius: 4px; border: 1px solid #ccc;'}),
        }
```

---

### Step 4: Write the CRUD Processing Center (Views)

We will compose five distinct logic states to manage the lifecycle of our data entries.

Open **`tickets/views.py`** and add this comprehensive logic structure:

```python
# tickets/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ProjectTicket
from .forms import TicketForm

# 1. READ ALL (Dashboard)
@login_required
def ticket_dashboard(request):
    # Fetch all items owned specifically by the current user
    user_tickets = ProjectTicket.objects.filter(user=request.user).order_by('-updated_at')
    return render(request, 'tickets/dashboard.html', {'tickets': user_tickets})

# 2. READ ONE (Detail View)
@login_required
def ticket_detail(request, pk):
    # Fetch item securely, ensure it belongs to the logged in user
    ticket = get_object_or_404(ProjectTicket, pk=pk, user=request.user)
    return render(request, 'tickets/detail.html', {'ticket': ticket})

# 3. CREATE
@login_required
def ticket_create(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            return redirect('ticket_dashboard')
    else:
        form = TicketForm()
    return render(request, 'tickets/ticket_form.html', {'form': form, 'action': 'Create New'})

# 4. UPDATE
@login_required
def ticket_update(request, pk):
    ticket = get_object_or_404(ProjectTicket, pk=pk, user=request.user)
    if request.method == 'POST':
        # passing instance=ticket hooks up the data to override the existing entry
        form = TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('ticket_detail', pk=ticket.pk)
    else:
        form = TicketForm(instance=ticket) # Pre-populate form fields
    return render(request, 'tickets/ticket_form.html', {'form': form, 'action': 'Edit'})

# 5. DELETE
@login_required
def ticket_delete(request, pk):
    ticket = get_object_or_404(ProjectTicket, pk=pk, user=request.user)
    if request.method == 'POST':
        ticket.delete()
        return redirect('ticket_dashboard')
    return render(request, 'tickets/delete_confirm.html', {'ticket': ticket})
```

---

### Step 5: Wire Up the Application Routing Paths

Let’s construct the routing mapping scheme to tie these view actions together with dynamic integer variables (`<int:pk>`) representing specific database IDs.

Create a brand new file inside the **`tickets`** folder named **`urls.py`**:

```python
# tickets/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.ticket_dashboard, name='ticket_dashboard'),
    path('ticket/<int:pk>/', views.ticket_detail, name='ticket_detail'),
    path('ticket/new/', views.ticket_create, name='ticket_create'),
    path('ticket/<int:pk>/edit/', views.ticket_update, name='ticket_update'),
    path('ticket/<int:pk>/delete/', views.ticket_delete, name='ticket_delete'),
]
```

Now connect this entire routing module straight to your central project router. Open **`core_project/urls.py`** and point the root directory directly to our new dashboard:

```python
# core_project/urls.py
from django.contrib import admin
from django.urls import path, include
from tickets.views import ticket_dashboard # 👈 Import our new landing target

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', ticket_dashboard, name='root_dashboard'), # 👈 Re-route the homepage target 
    path('workspace/', include('tickets.urls')), # 👈 Connects all CRUD operations
    path('old-tasks/', include('pages.urls')), 
]
```

---

### Step 6: Create the Front-End Presentation Templates

To render these views properly, we need to provide the template files we declared in the view logic.

Go to your main root **`templates`** folder and construct a brand-new directory inside it named **`tickets`**. This creates the `templates/tickets/` directory path.

#### Template A: The Central Dashboard (`templates/tickets/dashboard.html`)

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>DevTicket Dashboard</title>
</head>
<body style="font-family: Arial, sans-serif; background-color: #f8f9fa; margin: 0; padding: 20px;">
    
    <div style="background-color: #343a40; color: white; padding: 15px 30px; display: flex; justify-content: space-between; align-items: center; border-radius: 4px;">
        <h2>💻 DevTicket Hub</h2>
        <div>
            <span>Active Operator: <strong>{{ request.user.username }}</strong></span> | 
            <form method="POST" action="{% url 'logout' %}" style="display:inline; margin-left: 10px;">
                {% csrf_token %}<button type="submit" style="background:#dc3545; color:white; border:none; padding:5px 10px; border-radius:4px; cursor:pointer;">Exit</button>
            </form>
        </div>
    </div>

    <div style="margin: 25px 0; display: flex; justify-content: space-between; align-items: center;">
        <h3>My Active Tickets Workspace</h3>
        <a href="{% url 'ticket_create' %}" style="background-color: #28a745; color: white; padding: 10px 20px; text-decoration: none; border-radius: 4px; font-weight: bold;">+ Log New Ticket</a>
    </div>

    <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 100px)); gap: 20px;">
        {% for ticket in tickets %}
        <div style="background: white; border-left: 6px solid {% if ticket.priority == 'HIGH' %}#dc3545{% elif ticket.priority == 'MEDIUM' %}#ffc107{% else %}#17a2b8{% endif %}; padding: 20px; border-radius: 4px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
            <span style="font-size: 11px; background: #e9ecef; padding: 3px 8px; border-radius: 12px; font-weight: bold; text-transform: uppercase;">{{ ticket.status }}</span>
            <h4 style="margin: 12px 0 6px 0;">{{ ticket.title }}</h4>
            <p style="color: #6c757d; font-size: 13px; line-height: 1.4;">{{ ticket.description|truncatewords:15 }}</p>
            <hr style="border: 0; border-top: 1px solid #eee; margin: 15px 0;">
            <a href="{% url 'ticket_detail' ticket.pk %}" style="color: #007bff; text-decoration: none; font-size: 14px; font-weight: bold;">Inspect Track →</a>
        </div>
        {% empty %}
        <p style="color: #6c757d;">No workspace tickets currently registered. Click "+ Log New Ticket" to initialize development records.</p>
        {% endfor %}
    </div>

</body>
</html>
```

#### Template B: Dynamic Data Entry Form UI (`templates/tickets/ticket_form.html`)

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{{ action }} Ticket</title>
</head>
<body style="font-family: Arial, sans-serif; background-color: #f8f9fa; padding: 40px;">
    
    <div style="max-width: 600px; margin: 0 auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
        <h2>{{ action }} Ticket Entry</h2>
        <hr style="margin-bottom: 25px; border: 0; border-top: 1px solid #eee;">
        
        <form method="POST">
            {% csrf_token %}
            {{ form.as_p }}
            
            <div style="margin-top: 30px; display: flex; gap: 10px;">
                <button type="submit" style="background: #007bff; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; font-weight: bold;">
                    Commit Database Changes
                </button>
                <a href="{% url 'ticket_dashboard' %}" style="background: #6c757d; color: white; padding: 10px 20px; text-decoration: none; border-radius: 4px; font-size: 14px;">Cancel</a>
            </div>
        </form>
    </div>

</body>
</html>
```

#### Template C: Detail Record Breakdown (`templates/tickets/detail.html`)

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Ticket #{{ ticket.id }}</title>
</head>
<body style="font-family: Arial, sans-serif; background-color: #f8f9fa; padding: 40px;">

    <div style="max-width: 700px; margin: 0 auto; background: white; padding: 35px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <a href="{% url 'ticket_dashboard' %}" style="color: #6c757d; text-decoration: none; font-size: 14px;">← Back to Dashboard</a>
            <span style="font-size: 12px; color: #999;">Last Matrix Update: {{ ticket.updated_at }}</span>
        </div>
        
        <h1 style="margin: 20px 0 10px 0;">{{ ticket.title }}</h1>
        
        <div style="margin-bottom: 25px;">
            <span style="background: #343a40; color: white; padding: 4px 10px; border-radius: 4px; font-size: 12px; font-weight: bold;">Priority: {{ ticket.priority }}</span>
            <span style="background: #007bff; color: white; padding: 4px 10px; border-radius: 4px; font-size: 12px; font-weight: bold; margin-left: 5px;">Status: {{ ticket.status }}</span>
        </div>

        <div style="background: #f8f9fa; padding: 20px; border-radius: 4px; border: 1px solid #e9ecef; min-height: 150px; line-height: 1.6;">
            {{ ticket.description|linebreaks }}
        </div>

        <div style="margin-top: 35px; display: flex; gap: 15px;">
            <a href="{% url 'ticket_update' ticket.pk %}" style="background: #ffc107; color: #212529; text-decoration: none; padding: 10px 20px; border-radius: 4px; font-weight: bold; font-size: 14px;">Modify Ticket Data</a>
            <a href="{% url 'ticket_delete' ticket.pk %}" style="background: #dc3545; color: white; text-decoration: none; padding: 10px 20px; border-radius: 4px; font-weight: bold; font-size: 14px;">Wipe Entry From Database</a>
        </div>
    </div>

</body>
</html>
```

#### Template D: Data Deletion Safe Gatekeeper (`templates/tickets/delete_confirm.html`)

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Confirm Target Wiping</title>
</head>
<body style="font-family: Arial, sans-serif; background-color: #f8f9fa; padding: 40px;">

    <div style="max-width: 500px; margin: 50px auto; background: white; padding: 30px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); border-top: 6px solid #dc3545;">
        <h3>⚠️ Destructive Action Confirmation</h3>
        <p>Are you completely certain you want to delete the development ticket record: <strong>"{{ ticket.title }}"</strong>?</p>
        <p style="color: #dc3545; font-size: 13px;">This transaction is structural and cannot be undone.</p>
        
        <form method="POST" style="margin-top: 25px;">
            {% csrf_token %}
            <button type="submit" style="background: #dc3545; color: white; border: none; padding: 10px 20px; border-radius: 4px; cursor: pointer; font-weight: bold;">
                Yes, Purge Record
            </button>
            <a href="{% url 'ticket_detail' ticket.pk %}" style="background: #6c757d; color: white; padding: 10px 20px; text-decoration: none; border-radius: 4px; margin-left: 10px; font-size: 14px;">Abort</a>
        </form>
    </div>

</body>
</html>
```

---

### Step 7: Launch the Server and Run Full CRUD Checks

Fire up your backend system:

```bash
python manage.py runserver
```

Now, point your web browser to `http://127.0.0.1:8000/`.

1. **Gatekeeper Routing Verification:** You will automatically be blocked and redirected to the `/accounts/login/` security prompt. Log in with your established user.
2. **Create Verification:** Click **+ Log New Ticket**. Input a bug profile (e.g., Title: *"Fix payment processor integration error"*, Priority: *"HIGH"*), and click save.
3. **Read All Verification:** You will instantly drop back onto the dashboard, displaying your prioritized ticket item wrapped beautifully inside a color-coded card border.
4. **Read One Verification:** Click **Inspect Track →** to pull up the isolated detail page.
5. **Update Verification:** Click **Modify Ticket Data**, change the tracker status dropdown menu to *"In Progress"*, and save. The changes are immediately processed.
6. **Delete Verification:** Click **Wipe Entry From Database**, click the red validation button to confirm execution, and watch the system safely scrub the item completely from the persistent database tables.

---

### 🎓 Graduation Complete!
Congratulations! You have built a complete model-driven, user-isolated, authenticated web application using only native Django architecture tools. You've transformed from a framework beginner into a functional backend web engineer. Keep writing Python code and scaling your application architectures!