# Generated by Django 3.1.6 on 2021-03-08 04:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post_app', '0002_postapp_author'),
    ]

    operations = [
        migrations.RenameField(
            model_name='postapp',
            old_name='author',
            new_name='created_by',
        ),
    ]