from django.db import models
from Users.models import User
from Product.models import Product
from Order.models import Order
from django.conf import settings


# Create your models here.
class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    rating = models.DecimalField(decimal_places=2, max_digits=3)
    description = models.TextField()
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __str__(self):
        return f"Review by {self.user.email} for {self.product.title}"
