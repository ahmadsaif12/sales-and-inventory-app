from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Bill


class BillViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='bills-user',
            password='SafePassword123!',
        )

    def test_bill_list_requires_authentication(self):
        response = self.client.get(reverse('bill_list'))

        self.assertRedirects(
            response,
            f"{reverse('user-login')}?next={reverse('bill_list')}",
        )

    def test_bill_create_page_renders_for_an_authenticated_user(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse('bill_create'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Add bill record')


class BillModelTests(TestCase):
    def test_bill_has_a_readable_string_representation(self):
        bill = Bill.objects.create(
            institution_name='Power company',
            payment_details='Monthly electricity service',
            amount=125.50,
        )

        self.assertEqual(str(bill), 'Power company')
