# Generated by Django 5.0.2 on 2025-02-24 13:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0003_member_address_member_first_name_member_phone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='member',
            name='address',
        ),
        migrations.RemoveField(
            model_name='member',
            name='phone',
        ),
    ]
