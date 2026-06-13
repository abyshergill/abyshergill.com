import os
import re
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

class Category(models.Model):
    name = models.CharField(max_length=100)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['order']

    def __str__(self):
        return self.name

class Subject(models.Model):
    category = models.ForeignKey(Category, related_name='subjects', on_delete=models.SET_NULL, null=True, blank=True)
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
    TOPIC_LEVEL_CHOICES = [
        (2, 'Level 2 (##)'),
        (3, 'Level 3 (###)'),
    ]
    
    subject = models.ForeignKey(Subject, related_name='chapters', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(blank=True)
    content = models.TextField() # Markdown content
    file_path = models.CharField(max_length=500, blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    topic_level = models.PositiveSmallIntegerField(choices=TOPIC_LEVEL_CHOICES, default=2)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order']
        unique_together = ('subject', 'slug')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        
        # Security: Ensure file_path is within the project directory to prevent path traversal
        if self.file_path:
            # Normalize and check if the path is inside the project root
            base_dir = os.path.abspath(os.getcwd())
            target_path = os.path.abspath(self.file_path)
            
            if not target_path.startswith(base_dir):
                self.file_path = None # Disable sync if path is outside project
            
            # If saving (e.g. from admin) and we have a valid file_path, update the disk file
            if self.file_path and os.path.exists(self.file_path):
                try:
                    with open(self.file_path, 'r') as f:
                        disk_content = f.read()
                    if disk_content != self.content:
                        with open(self.file_path, 'w') as f:
                            f.write(self.content)
                except (OSError, IOError):
                    pass

        super().save(*args, **kwargs)

        # Remove code blocks before extracting topics to avoid false positives
        # Use non-greedy matching and multi-line support
        clean_content = re.sub(r'```[\s\S]*?```', '', self.content)
        clean_content = re.sub(r'~~~[\s\S]*?~~~', '', clean_content)
        # Remove inline code `...`
        clean_content = re.sub(r'`[^`]+`', '', clean_content)

        # Automatically extract topics from content based on chosen level
        prefix = '#' * self.topic_level
        # Regex explanation:
        # ^ - start of line
        # {prefix} - the exact number of # chosen
        # \s+ - at least one space
        # ([^\n]+) - capture everything until the end of the line
        pattern = rf'^{prefix}\s+([^\n]+)$'
        topics_found = re.findall(pattern, clean_content, re.MULTILINE)
        
        # Only update if topics have actually changed to avoid unnecessary DB writes
        existing_topics = list(self.topics.values_list('title', flat=True))
        if topics_found != existing_topics:
            self.topics.all().delete()
            for i, topic_title in enumerate(topics_found):
                Topic.objects.create(
                    chapter=self,
                    title=topic_title.strip(),
                    order=i
                )

    def __str__(self):
        return f"{self.subject.title} - {self.title}"

class Topic(models.Model):
    chapter = models.ForeignKey(Chapter, related_name='topics', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    slug = models.SlugField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        unique_together = ('chapter', 'slug')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.chapter.title} - {self.title}"

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
