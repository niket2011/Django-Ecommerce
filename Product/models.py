from django.db import models
from django.urls import reverse
import os
import random

# Create your models here.



class Product(models.Model):


    name=models.CharField(max_length=120)
    description=models.TextField(default=True)
    price=models.DecimalField(max_digits=10, decimal_places=2)
    slug = models.SlugField(max_length=100, db_index=True)
    image = models.ImageField(upload_to='Product/', null=True, blank=True)
    available = models.BooleanField(default=True)
    stock = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Product:product-detail",kwargs={"id":self.id})

class Order(models.Model):
        first_name = models.CharField(max_length=60)
        last_name = models.CharField(max_length=60)
        email = models.EmailField()
        address = models.CharField(max_length=150)
        postal_code = models.CharField(max_length=30)
        city = models.CharField(max_length=100)
        created = models.DateTimeField(auto_now_add=True)
        updated = models.DateTimeField(auto_now=True)
        paid = models.BooleanField(default=False)

        class Meta:
            ordering = ('-created',)

        def __str__(self):
            return 'Order {}'.format(self.id)

        def get_total_cost(self):
            return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity