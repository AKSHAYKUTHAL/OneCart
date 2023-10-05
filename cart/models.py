from django.db import models
from store.models import Product
from django.contrib.auth.models import User


class Cart(models.Model):
   
    cart_id = models.CharField(max_length=100, unique=True,default=0)  # Add this field
    # products = models.ManyToManyField(Product, through='CartItem')
    date_added=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Cart for {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    item_color = models.CharField(max_length=50,default='choose',null=True)
    item_size = models.CharField(max_length=50,default='choose',null=True)
    is_active=models.BooleanField(default=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.product_name}"
    
    def sub_total(self):
        return self.product.product_price*self.quantity
