from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password, is_password_usable
from lectures.models import UserProfile

class Command(BaseCommand):
    help = 'Hashes existing plain-text security answers'

    def handle(self, *args, **options):
        profiles = UserProfile.objects.all()
        count = 0
        for profile in profiles:
            # Simple check if it looks like a hash
            if not (profile.security_answer.startswith('pbkdf2_sha256$') or 
                    profile.security_answer.startswith('argon2$') or 
                    profile.security_answer.startswith('bcrypt$')):
                
                # Normalize plain text for hashing (lower and stripped as per views.py logic)
                raw_answer = profile.security_answer.strip().lower()
                profile.security_answer = make_password(raw_answer)
                profile.save()
                count += 1
        
        self.stdout.write(self.style.SUCCESS(f'Successfully hashed {count} security answers.'))
