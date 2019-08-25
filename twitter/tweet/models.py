from django.db import models
from django.contrib.auth.models import User

class Tweet(models.Model):
    """
    ツイートモデル
    bodyを入力して投稿する
    """
    user = models.ForeignKey(User, related_name='tweets', on_delete=models.CASCADE)
    body = models.CharField(max_length=140)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    fav_num = models.IntegerField(default=0)

    class Meta:
        # タイムラインを新着順にする
        ordering = ('-created_at',)
    
    def __str__(self):
        return self.body

class Fav(models.Model):
    favtweet = models.ForeignKey(Tweet, on_delete=models.DO_NOTHING,related_name='fav_number')
    fav_user = models.ForeignKey(User,on_delete=models.DO_NOTHING)