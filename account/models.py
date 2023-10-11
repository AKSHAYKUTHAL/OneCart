from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100,blank=True,)
    last_name = models.CharField(max_length=100,blank=True,)
    phone_number = models.CharField(max_length=100,blank=True)
    address_line_1 = models.CharField(blank=True, max_length=100)
    address_line_2 = models.CharField(blank=True, max_length=100)
    profile_picture = models.ImageField(blank=True, upload_to='userprofile')
    city = models.CharField(blank=True, max_length=20)
    state = models.CharField(blank=True, max_length=20)
    country = models.CharField(blank=True, max_length=20)
    zip_code = models.CharField(blank=True,default=123456)

    def __str__(self):
        return self.first_name

    def full_address(self):
        return f'{self.address_line_1} {self.address_line_2}'
    def email(self):
        return self.user.email

