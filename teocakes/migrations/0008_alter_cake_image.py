# Generated by Django 5.1.7 on 2025-03-19 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teocakes', '0007_alter_cake_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cake',
            name='image',
            field=models.ImageField(upload_to='images/'),
        ),
    ]
