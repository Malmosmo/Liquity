# Generated by Django 4.0 on 2021-12-31 11:33

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='profile.png', upload_to=users.models.upload_to),
        ),
        migrations.AlterField(
            model_name='profile',
            name='name',
            field=models.CharField(default='New User', max_length=16),
        ),
    ]