# Generated by Django 3.1.6 on 2021-03-25 05:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post_app', '0003_auto_20210308_1329'),
    ]

    operations = [
        migrations.AddField(
            model_name='postapp',
            name='title',
            field=models.CharField(max_length=25, null=True, verbose_name='タイトル'),
        ),
        migrations.AlterField(
            model_name='postapp',
            name='content',
            field=models.TextField(verbose_name='内容'),
        ),
    ]
