from django.db import models
from polls.models import CustumUser

class Tweet(models.Model):
    """
    ツイートモデル
    bodyを入力して投稿する
    """
    user = models.ForeignKey(CustumUser, related_name='tweets', on_delete=models.CASCADE)
    body = models.CharField(max_length=140)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(CustumUser, on_delete=models.CASCADE)
    favs = models.IntegerField(default=0)

    class Meta:
        # タイムラインを新着順にする
        ordering = ('-created_at',)
    
    def __str__(self):
        return self.body

class Fav(models.Model):
    favtweet = models.ForeignKey(Tweet, on_delete=models.DO_NOTHING,related_name='fav_number')
    fav_user = models.ForeignKey(CustumUser,on_delete=models.DO_NOTHING)