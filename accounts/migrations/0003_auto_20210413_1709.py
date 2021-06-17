# Generated by Django 3.1.6 on 2021-04-13 08:09

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20210204_2004'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='followees',
            field=models.ManyToManyField(blank=True, related_name='follower', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True, verbose_name='メールアドレス'),
        ),
        migrations.AlterField(
            model_name='user',
            name='followers',
            field=models.ManyToManyField(blank=True, related_name='followee', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='user',
            name='icon',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='アイコン画像'),
        ),
        migrations.AlterField(
            model_name='user',
            name='introduction',
            field=models.CharField(blank=True, max_length=75, null=True, verbose_name='自己紹介文'),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=25, unique=True, verbose_name='ユーザー名'),
        ),
    ]
