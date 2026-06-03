import markdown
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Subject, Chapter, QuestionAnswer
from .forms import ContactForm

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
                security_answer=form.cleaned_data['security_answer'],
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
    
    if request.method == 'POST':
        answer = request.POST.get('answer')
        if answer.strip().lower() == profile.security_answer.strip().lower():
            request.session['recovery_verified'] = True
            return redirect('forgot_password_reset')
        else:
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
        login_val = request.POST.get('username')
        password = request.POST.get('password')
        
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
            return redirect('home')
        else:
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
