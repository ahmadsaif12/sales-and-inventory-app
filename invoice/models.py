
from django.db import models
from store.models import Item
from django_extensions.db.fields import AutoSlugField


class Invoice(models.Model):
    """
    Represents an invoice for a purchased item.

    Attributes:
        slug (str): Unique slug based on the date.
        date (datetime): Date of invoice creation.
        customer_name (str): Name of the customer.
        contact_number (str): Customer's contact number.
        item (ForeignKey): The invoiced item.
        price_per_item (float): Price per item.
        quantity (float): Number of items purchased.
        shipping (float): Shipping charges.
        total (float): Total before shipping.
        grand_total (float): Total including shipping.
    """
    slug = AutoSlugField(
        unique=True,
        populate_from="date"
    )
    date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date (e.g., 2026/07/23)"
    )

    customer_name = models.CharField(max_length=100)

    contact_number = models.CharField(max_length=13)

    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE
    )
    price_per_item = models.FloatField(
        verbose_name="Price Per Item (Ksh)"
    )
    quantity = models.FloatField(default=0.00)
    shipping = models.FloatField(
        default=0.00,
        verbose_name="Shipping and Handling"
    )
    total = models.FloatField(
        verbose_name="Total Amount (Ksh)",
        editable=False
    )
    grand_total = models.FloatField(
        verbose_name="Grand Total (Ksh)",
        editable=False
    )

    def save(self, *args, **kwargs):
        """
        Calculate total and grand_total before saving.
        """
        self.total = round(
            self.quantity * self.price_per_item, 2
        )

        self.grand_total = round(
            self.total + self.shipping, 2
        )

        super().save(*args, **kwargs)

    def __str__(self):
        return self.slug