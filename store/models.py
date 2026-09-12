from django.db import models
from django.urls import reverse
from django.forms import model_to_dict
from django_extensions.db.fields import AutoSlugField
from phonenumber_field.modelfields import PhoneNumberField
from accounts.models import Vendor

class Category(models.Model):
    """
    Represents a category for items.
    """
    name = models.CharField(max_length=50)
    slug = AutoSlugField(unique=True, populate_from='name')

    def __str__(self):
        """
        String representation of the category.
        """
        return f"Category: {self.name}"

    class Meta:
        verbose_name_plural = 'Categories'

class Item(models.Model):
    slug = AutoSlugField(unique = True, populate_from = 'name')
    name = models.CharField(max_length = 50)
    description = models.TextField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    quantity = models.IntegerField(default =0)
    price  = models.FloatField(default=0)
    expiring_date = models.DateTimeField(null = True, blank=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return {
            f"{self.name} - Category : {self.category},"
            f"Quantity : {self.quantity}"
        }

    def abolute_url(self):
        #returns absolute urls for an item detail view
        return reverse('item-detail' , kwargs={'slug' : self.slug})

    def to_json(self):
        product = model_to_dict(self)
        product['id'] = self.id
        product['text'] = self.name
        product['category'] = self.category.name
        product['quantity'] = 1
        product['total_product'] = 0
        return product

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'items'

class Delivery(models.Model):
    """
    reprensents a delivery item to the customers
    """
    item = models.ForeignKey(Item, blank=True,null=True ,on_delete=models.SET_NULL)
    customer_name = models.CharField(max_length=50, blank=True,null=True)
    phone_number = PhoneNumberField(blank=True,null=True)
    location = models.CharField(max_length=50, blank=True,null=True)
    date = models.DateTimeField()
    is_delivered = models.BooleanField(default=False,verbose_name='Is Delivered')

    def __str__(self):
        return {
        f"Delivery of {self.item} to {self.customer_name}"
        f"at {self.location} on {self.date}"
        }