import markdown
import time
import os
from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.hashers import make_password, check_password
from .models import Subject, Chapter, QuestionAnswer, LoginAttempt, UserProfile
from .forms import ContactForm

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def get_login_delay(username, ip_address):
    attempt, created = LoginAttempt.objects.get_or_create(username=username, ip_address=ip_address)
    if attempt.failures < 3:
        return 0, attempt
    delay = (attempt.failures - 2) * 10
    return delay, attempt

def home(request):
    subjects = Subject.objects.all()
    return render(request, 'home.html', {'subjects': subjects})

def qa_list(request):
    qas = QuestionAnswer.objects.all().order_by('-created_at')
    return render(request, 'qa_list.html', {'qas': qas})

def search(request):
    query = request.GET.get('q')
    subjects = []
    chapters = []
    if query:
        subjects = Subject.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
        chapters = Chapter.objects.filter(Q(title__icontains=query) | Q(content__icontains=query))
    
    return render(request, 'search_results.html', {
        'query': query,
        'subjects': subjects,
        'chapters': chapters
    })

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'contact.html', {'form': ContactForm(), 'success': True})
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Subject, Chapter, QuestionAnswer, UserProfile
from .forms import ContactForm, SignupForm

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            UserProfile.objects.create(
                user=user,
                security_question=form.cleaned_data['security_question'],
                security_answer=make_password(form.cleaned_data['security_answer'].strip().lower()),
                security_hint=form.cleaned_data['security_hint']
            )
            login(request, user)
            messages.success(request, "Account created successfully!")
            return redirect('home')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})

def forgot_password_step1(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        try:
            user = User.objects.get(Q(username=username) | Q(email=username))
            request.session['recovery_user_id'] = user.id
            return redirect('forgot_password_step2')
        except User.DoesNotExist:
            messages.error(request, "User not found.")
    return render(request, 'forgot_password_step1.html')

def forgot_password_step2(request):
    user_id = request.session.get('recovery_user_id')
    if not user_id:
        return redirect('forgot_password_step1')
    
    user = User.objects.get(id=user_id)
    profile = user.profile
    ip_address = get_client_ip(request)
    # Use user_id as identifier for recovery attempts
    attempt_id = f"recovery_{user_id}"
    delay, attempt = get_login_delay(attempt_id, ip_address)

    if request.method == 'POST':
        if delay > 0:
            last_attempt_time = attempt.last_attempt
            time_since_last = (timezone.now() - last_attempt_time).total_seconds()
            if time_since_last < delay:
                wait_time = int(delay - time_since_last)
                messages.error(request, f"Too many failed attempts. Please wait {wait_time} seconds.")
                return render(request, 'forgot_password_step2.html', {
                    'question': profile.security_question,
                    'hint': profile.security_hint
                })

        answer = request.POST.get('answer')
        if check_password(answer.strip().lower(), profile.security_answer):
            request.session['recovery_verified'] = True
            attempt.failures = 0
            attempt.save()
            return redirect('forgot_password_reset')
        else:
            attempt.failures += 1
            attempt.save()
            messages.error(request, "Incorrect answer.")
            
    return render(request, 'forgot_password_step2.html', {
        'question': profile.security_question,
        'hint': profile.security_hint
    })

def forgot_password_reset(request):
    if not request.session.get('recovery_verified'):
        return redirect('forgot_password_step1')
    
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password == confirm_password:
            user_id = request.session.get('recovery_user_id')
            user = User.objects.get(id=user_id)
            user.set_password(password)
            user.save()
            del request.session['recovery_user_id']
            del request.session['recovery_verified']
            messages.success(request, "Password reset successfully!")
            return redirect('login')
        else:
            messages.error(request, "Passwords do not match.")
            
    return render(request, 'forgot_password_reset.html')

def logout_view(request):
    logout(request)
    return redirect('home')

def login_view(request):
    if request.method == 'POST':
        login_val = request.POST.get('login') # Fixed from 'username' to 'login'
        password = request.POST.get('password')
        
        if not login_val:
            messages.error(request, "Username or Email is required.")
            return render(request, 'login.html')

        ip_address = get_client_ip(request)
        delay, attempt = get_login_delay(login_val, ip_address)
        
        if delay > 0:
            last_attempt_time = attempt.last_attempt
            time_since_last = (timezone.now() - last_attempt_time).total_seconds()
            if time_since_last < delay:
                wait_time = int(delay - time_since_last)
                messages.error(request, f"Too many failed attempts. Please wait {wait_time} seconds.")
                return render(request, 'login.html')

        # Try to find a user by username or email
        user = None
        if '@' in login_val:
            try:
                email_user = User.objects.get(email=login_val)
                user = authenticate(request, username=email_user.username, password=password)
            except User.DoesNotExist:
                pass
        
        if user is None:
            user = authenticate(request, username=login_val, password=password)
            
        if user is not None:
            login(request, user)
            attempt.failures = 0
            attempt.save()
            return redirect('home')
        else:
            attempt.failures += 1
            attempt.save()
            messages.error(request, "Invalid username or password.")
            return render(request, 'login.html')
    return render(request, 'login.html')

def subject_detail(request, subject_slug, chapter_slug=None):
    subject = get_object_or_404(Subject, slug=subject_slug)
    chapters = subject.chapters.all()
    
    if chapter_slug:
        current_chapter = get_object_or_404(Chapter, subject=subject, slug=chapter_slug)
    else:
        current_chapter = chapters.first()
        
    if current_chapter and current_chapter.file_path:
        # Sync based on modification time to avoid overwriting newer Admin changes
        if os.path.exists(current_chapter.file_path):
            file_mtime = timezone.datetime.fromtimestamp(os.path.getmtime(current_chapter.file_path), tz=timezone.get_current_timezone())
            
            # If disk file is significantly newer than database record, sync from disk
            # We use a small buffer (e.g. 1 second) to account for filesystem precision
            if file_mtime > current_chapter.updated_at + timezone.timedelta(seconds=1):
                with open(current_chapter.file_path, 'r') as f:
                    disk_content = f.read()
                if disk_content != current_chapter.content:
                    current_chapter.content = disk_content
                    # We use .save() which will also trigger Chapter.save() to write back,
                    # but since content is now same as disk, it's safe.
                    current_chapter.save()

    content_html = ""
    if current_chapter:
        # Convert markdown to HTML
        md = markdown.Markdown(extensions=['extra', 'codehilite', 'toc'])
        content_html = md.convert(current_chapter.content)
        
        # Post-processing: wrap pre/code in code-container for our CSS
        # This is a simple replacement, for more complex ones we could use a markdown extension
        content_html = content_html.replace('<pre>', '<div class="code-container relative group"><button class="copy-code-btn">Copy</button><pre>')
        content_html = content_html.replace('</pre>', '</pre></div>')

    return render(request, 'subject_detail.html', {
        'subject': subject,
        'chapters': chapters,
        'current_chapter': current_chapter,
        'content_html': content_html,
    })
