# Generated by Django 5.1.7 on 2025-03-29 11:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teocakes', '0013_transaction'),
    ]

    operations = [
        migrations.RenameField(
            model_name='transaction',
            old_name='ref',
            new_name='tx_ref',
        ),
    ]
