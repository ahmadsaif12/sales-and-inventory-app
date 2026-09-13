from django.test import TestCase
from django.contrib.auth.models import User


class RegisterAuthToastsTest(TestCase):
    def test_register_page_has_no_help_text_or_usable_password(self):
        resp = self.client.get('/accounts/register/')
        self.assertEqual(resp.status_code, 200)
        html = resp.content.decode()
        self.assertNotIn('usable_password', html)
        self.assertNotIn('150 characters or fewer', html)

    def test_register_creates_user_and_toast_on_login(self):
        resp = self.client.post('/accounts/register/', {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'SuperSecret12!',
            'password2': 'SuperSecret12!',
        })
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(User.objects.filter(username='testuser').exists())

        login_page = self.client.get('/accounts/login/')
        html = login_page.content.decode()
        self.assertIn('Your account has been created', html)

    def test_login_emits_welcome_toast(self):
        User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='SuperSecret12!',
        )
        resp = self.client.post('/accounts/login/', {
            'username': 'testuser',
            'password': 'SuperSecret12!',
        })
        self.assertEqual(resp.status_code, 302)

        profile_page = self.client.get('/accounts/profile/')
        html = profile_page.content.decode()
        self.assertIn('Welcome back, testuser', html)