# Generated by Django 4.2.5 on 2023-10-03 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0005_cartitem_item_color_cartitem_item_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='item_color',
            field=models.CharField(default='choose', max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='item_size',
            field=models.CharField(default='choose', max_length=50, null=True),
        ),
    ]
