from django.db import models
from django.urls import reverse
from home.models import Categories


class ProductColor(models.Model):
    name = models.CharField(max_length=50,default='nil')

    def __str__(self):
        return self.name

class ProductSize(models.Model):
    name = models.CharField(max_length=50, default='')

    def __str__(self):
        return self.name

class Product(models.Model):

    product_name = models.CharField(max_length=100)
    product_slug = models.SlugField(unique=True)
    product_description = models.TextField()
    product_price = models.IntegerField(default=0)
    product_image = models.ImageField(upload_to='picture')
    product_stock = models.IntegerField(default=0)
    product_is_available = models.BooleanField(default=False)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    product_created_date = models.DateTimeField(auto_now_add=True)
    product_modified_date = models.DateTimeField(auto_now_add=True)
    product_colors = models.ManyToManyField(ProductColor, blank=True,null=True) 
    product_sizes = models.ManyToManyField(ProductSize, blank=True,null=True)  

    def __str__(self):
        return self.product_name

    def get_url(self):
        return reverse('product_details', args=[self.category.category_slug, self.product_slug])


