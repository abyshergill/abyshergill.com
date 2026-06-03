from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    security_question = models.CharField(max_length=255)
    security_answer = models.CharField(max_length=255)
    security_hint = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Profile for {self.user.username}"

class Subject(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    icon = models.CharField(max_length=10, default='📚') # Emoji icon

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class Chapter(models.Model):
    subject = models.ForeignKey(Subject, related_name='chapters', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(blank=True)
    content = models.TextField() # Markdown content
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        unique_together = ('subject', 'slug')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.subject.title} - {self.title}"

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.name} - {self.subject}"

class QuestionAnswer(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question
