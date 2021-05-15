# Generated by Django 3.2.3 on 2021-05-14 09:01

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_auto_20210514_0008'),
    ]

    operations = [
        migrations.CreateModel(
            name='CareInstructions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('instruction_name', models.CharField(max_length=255, unique=True)),
                ('cares_details', ckeditor_uploader.fields.RichTextUploadingField()),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('write_date', models.DateTimeField(auto_now=True)),
                ('active', models.BooleanField(default=True)),
                ('changed_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='care_changed_by', to=settings.AUTH_USER_MODEL)),
                ('created_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'care instructions',
            },
        ),
        migrations.AddField(
            model_name='product',
            name='instruction_ids',
            field=models.ManyToManyField(blank=True, to='shop.CareInstructions'),
        ),
    ]