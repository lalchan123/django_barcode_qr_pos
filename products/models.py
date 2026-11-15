from django.db import models
from django.utils.text import slugify
import uuid

class Product(models.Model):
    BARCODE_CHOICES = [("code128", "Code 128"), ("ean13", "EAN-13")]
    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=60, unique=True)
    barcode = models.CharField(max_length=100, unique=True)
    barcode_type = models.CharField(max_length=20, choices=BARCODE_CHOICES, default="code128")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.barcode})"
