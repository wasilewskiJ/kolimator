# Generated by Django 4.2.11 on 2024-06-30 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0007_currentsetting_crosshair_size_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='currentsetting',
            name='laser',
            field=models.BooleanField(default=False),
        ),
    ]
