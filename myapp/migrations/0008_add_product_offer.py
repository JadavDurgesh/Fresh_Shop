# Generated by Django 5.0.2 on 2024-03-12 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_rename_add_products_add_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='add_product',
            name='offer',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
