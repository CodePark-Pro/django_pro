from django.db import models
#from accounts.models import User
from django.contrib.auth import get_user_model
# Create your models here.

class PostApp(models.Model):
    title = models.CharField(max_length=25, verbose_name='タイトル',null=True)
    content = models.TextField(verbose_name='内容')
    created_at = models.DateTimeField(auto_now_add=True)
    #投稿したユーザーとモデルを紐づけ
    created_by = models.ForeignKey(get_user_model(),on_delete=models.CASCADE,null=True)
    image1 = models.ImageField(upload_to='images/',blank=True, null=True, verbose_name='投稿画像1')
    image2 = models.ImageField(upload_to='images/',blank=True, null=True, verbose_name='投稿画像2')
    image3 = models.ImageField(upload_to='images/',blank=True, null=True, verbose_name='投稿画像3')
    map_addrs = models.CharField(max_length=30, verbose_name='地図住所',blank=True, null=True)
    

    def __str__(self):
        return self.content
