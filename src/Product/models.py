from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


# Create your models here.
class Category(MPTTModel):
    name = models.CharField(max_length=100)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']
        level_attr = 'mptt_level'
        lft_attr = 'mptt_left'
        rght_attr = 'mptt_right'
        tree_id_attr = 'mptt_tree_id'

    def __str__(self):
        return self.name

    def get_category_tree(self):
        return self.get_descendants(include_self=True)


class Product(models.Model):
    title = models.CharField(max_length=255)
    brand = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title

class AttributeType(models.Model):
    name= models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ProductAttribute(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='attributes')
    attribute_name = models.ForeignKey(AttributeType, on_delete=models.CASCADE)
    attribute_value = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.attribute_name}: {self.attribute_value}"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image_url = models.URLField()

    def __str__(self):
        return self.image_url
