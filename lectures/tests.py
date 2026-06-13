from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from lectures.models import Subject, Chapter, LoginAttempt
from django.utils import timezone

class SecurityTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('signup')
        self.login_url = reverse('login')

    def test_password_validation(self):
        # Test weak password
        response = self.client.post(self.signup_url, {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': '123',
            'confirm_password': '123',
            'security_question': 'Question?',
            'security_answer': 'Answer',
        })
        # Check if "This password is too short" or similar is in response content
        self.assertContains(response, "too short", status_code=200)

    def test_markdown_sanitization(self):
        subject = Subject.objects.create(title='Test Subject', description='Test')
        chapter = Chapter.objects.create(
            subject=subject,
            title='Test Chapter',
            content='<script>alert("xss")</script> **Bold**'
        )
        url = reverse('subject_detail', args=[subject.slug])
        response = self.client.get(url)
        # Bleach should escape the script tag
        self.assertContains(response, '&lt;script&gt;alert("xss")&lt;/script&gt;')
        self.assertContains(response, '<strong>Bold</strong>')

    def test_login_throttling_logic(self):
        # Fail 3 times
        for i in range(3):
            self.client.post(self.login_url, {
                'login': 'throttle_me',
                'password': 'wrongpassword'
            })

        attempt = LoginAttempt.objects.get(username='throttle_me')
        self.assertEqual(attempt.failures, 3)

        # 4th attempt should be throttled
        response = self.client.post(self.login_url, {
            'login': 'throttle_me',
            'password': 'wrongpassword'
        })
        self.assertContains(response, "Too many failed attempts")

        # Failures should still be 3 because it didn't even try to authenticate
        attempt.refresh_from_db()
        self.assertEqual(attempt.failures, 3)
