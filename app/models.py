from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)


class Purchase(models.Model):
    items = models.ManyToManyField('PurchaseItem')
    total = models.PositiveIntegerField()
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now())


class PurchaseItem(models.Model):
    product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveSmallIntegerField(default=1)
    subtotal = models.PositiveIntegerField()

