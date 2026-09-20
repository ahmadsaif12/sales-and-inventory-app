from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.staticfiles import finders
from django.urls import reverse

from .models import Category, Item


class DashboardPresentationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='store-user',
            password='SafePassword123!',
        )

    def test_dashboard_requires_authentication(self):
        response = self.client.get(reverse('dashboard'))

        self.assertRedirects(
            response,
            f"{reverse('user-login')}?next={reverse('dashboard')}",
        )

    def test_dashboard_uses_the_shared_application_shell(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse('dashboard'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'class="dashboard-body"')
        self.assertContains(response, 'class="app-content"')

    def test_shared_dashboard_stylesheet_is_available(self):
        stylesheet = finders.find('css/style.css')

        self.assertIsNotNone(stylesheet)
        with open(stylesheet, encoding='utf-8') as css_file:
            stylesheet_contents = css_file.read()
        self.assertIn('--app-primary', stylesheet_contents)
        self.assertIn('.app-content .table', stylesheet_contents)


class ItemModelTests(TestCase):
    def test_item_json_contains_the_data_needed_by_item_search(self):
        category = Category.objects.create(name='Office supplies')
        item = Item.objects.create(
            name='Notebook',
            description='Hardcover notebook',
            category=category,
            quantity=7,
            price=4.5,
        )

        item_data = item.to_json()

        self.assertEqual(item_data['id'], item.pk)
        self.assertEqual(item_data['text'], 'Notebook')
        self.assertEqual(item_data['category'], 'Office supplies')
        self.assertEqual(item_data['quantity'], 1)
