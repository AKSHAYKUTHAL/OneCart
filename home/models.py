from django.db import models
from django.urls import reverse



class Categories(models.Model):
    category_name = models.CharField(max_length=50)
    category_slug = models.SlugField(unique=True)
    category_description = models.TextField()
    category_image = models.ImageField(upload_to='picture')

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


    def __str__(self):
        return self.category_name
    
    def get_url(self):
        return reverse('category_sort',args=[self.category_slug])


