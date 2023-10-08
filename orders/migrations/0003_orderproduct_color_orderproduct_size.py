# Generated by Django 4.2.5 on 2023-10-08 04:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_alter_product_product_colors_and_more'),
        ('orders', '0002_remove_orderproduct_color_remove_orderproduct_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderproduct',
            name='color',
            field=models.ManyToManyField(blank=True, to='store.productcolor'),
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='size',
            field=models.ManyToManyField(blank=True, to='store.productsize'),
        ),
    ]
