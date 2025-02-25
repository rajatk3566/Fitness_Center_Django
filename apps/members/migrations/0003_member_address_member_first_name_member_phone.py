# Generated by Django 5.0.2 on 2025-02-24 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0002_remove_member_address_remove_member_created_at_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='address',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='member',
            name='first_name',
            field=models.CharField(default='member', max_length=255),
        ),
        migrations.AddField(
            model_name='member',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
