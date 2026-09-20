from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from accounts.models import Customer
from store.models import Category, Item

from .forms import PurchaseForm
from .models import Sale, SaleDetail


class TransactionViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='transactions-user',
            password='SafePassword123!',
        )

    def test_sales_list_requires_authentication(self):
        response = self.client.get(reverse('saleslist'))

        self.assertRedirects(
            response,
            f"{reverse('user-login')}?next={reverse('saleslist')}",
        )

    def test_transaction_list_urls_are_available_for_sidebar_navigation(self):
        self.assertEqual(reverse('saleslist'), '/transactions/sales/')
        self.assertEqual(reverse('purchaseslist'), '/transactions/purchases/')

    def test_sale_create_page_renders_with_its_customer_search_route(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse('sale-create'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, reverse('get_customers'))


class TransactionModelAndFormTests(TestCase):
    def test_sale_counts_its_detail_quantities(self):
        customer = Customer.objects.create(first_name='Mina', last_name='Shrestha')
        category = Category.objects.create(name='Stationery')
        item = Item.objects.create(
            name='Pen',
            description='Blue ink pen',
            category=category,
            quantity=20,
            price=2.5,
        )
        sale = Sale.objects.create(customer=customer, sub_total=7.5, grand_total=7.5)
        SaleDetail.objects.create(
            sale=sale,
            item=item,
            price=2.5,
            quantity=3,
            total_detail=7.5,
        )

        self.assertEqual(sale.sum_products(), 3)

    def test_purchase_form_exposes_only_editable_purchase_fields(self):
        form = PurchaseForm()

        self.assertNotIn('total_value', form.fields)
        self.assertEqual(
            list(form.fields),
            [
                'item', 'price', 'description', 'vendor', 'quantity',
                'delivery_date', 'delivery_status',
            ],
        )
