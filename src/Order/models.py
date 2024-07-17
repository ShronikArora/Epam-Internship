from django.db import models
from django.db.models import Sum, F
from Users.models import Address
from Product.models import Product
from django.conf import settings
from decimal import Decimal, ROUND_HALF_UP


# Create your models here.
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True)
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"Order {self.id} by {self.user.email}"

    @property
    def total_price(self):
        total = self.items.aggregate(total=Sum(F("price") * F("quantity")))["total"]
        return Decimal(total or 0.0).quantize(Decimal('0.00'), rounding=ROUND_HALF_UP)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} of {self.product.title} in order {self.order.id}"
