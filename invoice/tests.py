from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from store.models import Category, Item

from .models import Invoice


class InvoiceViewsTest(TestCase):
    def test_invoice_list_requires_authentication(self):
        response = self.client.get(reverse('invoicelist'))

        self.assertRedirects(
            response,
            f"{reverse('user-login')}?next={reverse('invoicelist')}",
        )


class InvoiceModelTests(TestCase):
    def test_invoice_calculates_totals_when_saved(self):
        category = Category.objects.create(name='Accessories')
        item = Item.objects.create(
            name='USB cable',
            description='One metre USB-C cable',
            category=category,
            quantity=10,
            price=5,
        )
        invoice = Invoice.objects.create(
            customer_name='Ravi Kumar',
            contact_number='5551234567',
            item=item,
            price_per_item=12.5,
            quantity=2,
            shipping=3.25,
        )

        self.assertEqual(invoice.total, 25)
        self.assertEqual(invoice.grand_total, 28.25)
