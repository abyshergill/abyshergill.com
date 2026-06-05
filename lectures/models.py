import os
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
    file_path = models.CharField(max_length=500, blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']
        unique_together = ('subject', 'slug')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        
        # If saving (e.g. from admin) and we have a file_path, update the disk file
        if self.file_path and os.path.exists(self.file_path):
            try:
                # Avoid circular sync by checking if disk is already same
                with open(self.file_path, 'r') as f:
                    disk_content = f.read()
                if disk_content != self.content:
                    with open(self.file_path, 'w') as f:
                        f.write(self.content)
            except Exception:
                pass

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.subject.title} - {self.title}"

class ChapterImage(models.Model):
    chapter = models.ForeignKey(Chapter, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='chapter_images/')
    caption = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Image for {self.chapter.title}"

    @property
    def markdown_tag(self):
        return f"![{self.caption or 'image'}]({self.image.url})"

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

class LoginAttempt(models.Model):
    username = models.CharField(max_length=255, db_index=True)
    ip_address = models.GenericIPAddressField(db_index=True)
    failures = models.IntegerField(default=0)
    last_attempt = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('username', 'ip_address')

    def __str__(self):
        return f"{self.username} from {self.ip_address} - {self.failures} failures"
