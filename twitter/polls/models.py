from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import m2m_changed

class CustumUser(AbstractUser):
    follow_num = models.IntegerField(default=0)
    follower_num = models.IntegerField(default=0)
    following = models.ManyToManyField('self', related_name='is_follow', symmetrical=False, blank=True)
    followers = models.ManyToManyField('self', related_name='followed_by', symmetrical=False, blank=True)
    profile = models.TextField(verbose_name='write your profile here', blank=True, max_length=256)

    class Meta:
        # タイムラインを新着順にする
        ordering = ('id',)

def follow_num_change(sender, instance, action, **kwargs):
    if action.startswith("post_"):
        instance.follow_num = instance.following.count()
        instance.save()
m2m_changed.connect(follow_num_change, sender=CustumUser.following.through)

def follower_num_change(sender, instance, action, **kwargs):
    if action.startswith("post_"):
        instance.follower_num = instance.followers.count()
        instance.save()
m2m_changed.connect(follower_num_change, sender=CustumUser.followers.through)


class Poll(models.Model):
    question = models.CharField(max_length=100)
    created_by = models.ForeignKey(CustumUser, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question

class Choice(models.Model):
    poll = models.ForeignKey(Poll, related_name='choices', on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=100)

    def __str__(self):
        return self.choice_text

class Vote(models.Model):
    choice = models.ForeignKey(Choice, related_name='vote', on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    voted_by = models.ForeignKey(CustumUser, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("poll", "voted_by")