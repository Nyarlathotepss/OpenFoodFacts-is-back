# Generated by Django 3.0b1 on 2020-02-12 19:42

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products_app', '0007_auto_20200211_1411'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='favorite_of',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Favorite',
        ),
    ]
