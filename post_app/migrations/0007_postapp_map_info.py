# Generated by Django 3.1.6 on 2021-05-19 04:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post_app', '0006_auto_20210519_1239'),
    ]

    operations = [
        migrations.AddField(
            model_name='postapp',
            name='map_info',
            field=models.CharField(max_length=30, null=True, verbose_name='地図情報'),
        ),
    ]
