# Generated by Django 4.2.5 on 2023-09-28 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0002_cart_cart_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='products',
        ),
        migrations.AddField(
            model_name='cart',
            name='date_added',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='cartitem',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
