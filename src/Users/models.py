from django.db import models


# Create your models here.
class User(models.Model):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email


class Address(models.Model):
    address_line = models.CharField(max_length=400)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.address_line}, {self.city}, {self.state}, {self.country}"
