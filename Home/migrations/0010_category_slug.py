# Generated by Django 5.1.1 on 2024-10-07 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Home', '0009_contact'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, unique=True),
        ),
    ]
