# Generated by Django 4.2.5 on 2023-10-03 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_product_product_color_product_product_size'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductColor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='nil', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ProductSize',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('S', 'Small'), ('M', 'Medium'), ('L', 'Large'), ('XL', 'XL'), ('XXL', 'XXL')], default='nil', max_length=50)),
            ],
        ),
        migrations.RemoveField(
            model_name='product',
            name='product_color',
        ),
        migrations.RemoveField(
            model_name='product',
            name='product_size',
        ),
        migrations.AddField(
            model_name='product',
            name='product_colors',
            field=models.ManyToManyField(to='store.productcolor'),
        ),
        migrations.AddField(
            model_name='product',
            name='product_sizes',
            field=models.ManyToManyField(to='store.productsize'),
        ),
    ]
