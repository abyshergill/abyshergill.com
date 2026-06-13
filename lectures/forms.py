from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .models import ContactMessage, UserProfile

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'input-field', 'placeholder': 'Your Email'}),
            'subject': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Subject'}),
            'message': forms.Textarea(attrs={'class': 'input-field', 'placeholder': 'How can we help?', 'rows': 5}),
        }

class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input-field', 'placeholder': '••••••••'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input-field', 'placeholder': '••••••••'}))
    security_question = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'e.g., What is your first pet\'s name?'}))
    security_answer = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Your answer'}))
    security_hint = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Hint for your answer (optional)'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'johndoe'}),
            'email': forms.EmailInput(attrs={'class': 'input-field', 'placeholder': 'john@example.com'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        user = User(username=cleaned_data.get('username'), email=cleaned_data.get('email'))

        if password:
            try:
                validate_password(password, user)
            except forms.ValidationError as e:
                self.add_error('password', e)

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data
