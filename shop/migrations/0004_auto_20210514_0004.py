# Generated by Django 3.2.3 on 2021-05-13 18:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_auto_20210514_0004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='color',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 5, 14, 0, 4, 36, 862997)),
        ),
        migrations.AlterField(
            model_name='product',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 5, 14, 0, 4, 36, 862997)),
        ),
        migrations.AlterField(
            model_name='size',
            name='create_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2021, 5, 14, 0, 4, 36, 862997)),
        ),
    ]