from django.db import models
from django.urls import reverse
from home.models import Categories
from django.contrib.auth.models import User
from django.db.models import Avg,Count


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
    product_colors = models.ManyToManyField(ProductColor, blank=True,) 
    product_sizes = models.ManyToManyField(ProductSize, blank=True)  

    def __str__(self):
        return self.product_name

    def get_url(self):
        return reverse('product_details', args=[self.category.category_slug, self.product_slug])
    
    def average_review(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(average=Avg('rating'))
        avg = 0
        if reviews['average'] is not None:
            avg = float(reviews['average'])
        return avg

    def count_review(self):
        reviews = ReviewRating.objects.filter(product=self, status=True).aggregate(count=Count('id'))
        count = 0
        if reviews['count'] is not None:
            count = int(reviews['count'])
        return count


class ReviewRating(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100, blank=True)
    review = models.TextField(max_length=500, blank=True)
    rating = models.FloatField()
    ip = models.CharField(max_length=20, blank=True)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject					
    

class ProductGallery(models.Model):
    product = models.ForeignKey(Product, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='store/products', max_length=255)

    def __str__(self):
        return self.product.product_name

    class Meta:
        verbose_name = 'productgallery'
        verbose_name_plural = 'product gallery'