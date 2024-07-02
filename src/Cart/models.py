from django.db import models
from Users.models import User
from Product.models import Product
from django.conf import settings


# Create your models here.
class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.quantity} of {self.product.title} "
