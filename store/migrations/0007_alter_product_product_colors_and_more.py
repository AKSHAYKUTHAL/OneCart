# Generated by Django 4.2.5 on 2023-10-04 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_alter_product_product_colors_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_colors',
            field=models.ManyToManyField(blank=True, null=True, to='store.productcolor'),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_sizes',
            field=models.ManyToManyField(blank=True, null=True, to='store.productsize'),
        ),
    ]
