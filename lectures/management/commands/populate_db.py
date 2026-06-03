import os
import re
from django.core.management.base import BaseCommand
from lectures.models import Subject, Chapter

class Command(BaseCommand):
    help = 'Populate the database with initial subjects and chapters'

    def handle(self, *args, **options):
        base_dir = '/home/aby/Downloads/Main'
        
        # Define subjects to import
        subjects_to_import = [
            {'title': 'Django', 'dir': 'Django', 'icon': '🎸'},
            {'title': 'Markdown', 'dir': 'Markdown', 'icon': '📝'},
            # Python content will be handled specially or manually if needed
        ]

        for sub_data in subjects_to_import:
            subject, created = Subject.objects.get_or_create(
                title=sub_data['title'],
                defaults={'description': f"Learn everything about {sub_data['title']} in this comprehensive course.", 'icon': sub_data['icon']}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created Subject: {subject.title}"))

            subject_dir = os.path.join(base_dir, sub_data['dir'])
            if not os.path.exists(subject_dir):
                continue

            # List directories and sort them by Chapter number
            chapters_dirs = [d for d in os.listdir(subject_dir) if os.path.isdir(os.path.join(subject_dir, d))]
            # Simple sorting by name should work for "Chapter_1", "Chapter_2", etc.
            chapters_dirs.sort()

            for i, chapter_dir in enumerate(chapters_dirs):
                readme_path = os.path.join(subject_dir, chapter_dir, 'README.md')
                if os.path.exists(readme_path):
                    with open(readme_path, 'r') as f:
                        content = f.read()
                    
                    # Try to extract a clean title from the directory name
                    # e.g., "Chapter_1_Introduction_Environment_Setup" -> "Chapter 1: Introduction Environment Setup"
                    title = chapter_dir.replace('_', ' ').replace('Chapter ', 'Chapter ')
                    if 'Chapter' not in title:
                         title = f"Chapter {i+1}: {title}"
                    
                    chapter, created = Chapter.objects.update_or_create(
                        subject=subject,
                        slug=chapter_dir.lower().replace('_', '-'),
                        defaults={
                            'title': title,
                            'content': content,
                            'order': i
                        }
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f"  Created Chapter: {chapter.title}"))

        # Add a Python subject manually since it's just an HTML file in the root
        python_subject, created = Subject.objects.get_or_create(
            title='Python',
            defaults={'description': 'Master Python programming from scratch.', 'icon': '🐍'}
        )
        if created:
             # Just add one chapter for Python as a placeholder
             Chapter.objects.get_or_create(
                 subject=python_subject,
                 title='Chapter 1: Welcome to Python',
                 slug='welcome-to-python',
                 defaults={
                     'content': '# Welcome to Python\n\nPython is a high-level, interpreted programming language known for its clear syntax and dynamic readability.',
                     'order': 0
                 }
             )
             self.stdout.write(self.style.SUCCESS("Created Subject: Python"))

        self.stdout.write(self.style.SUCCESS("Database population complete!"))
