from rest_framework import generics, status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Fav, Tweet
from .serializers import FavSerializer, TweetSerializer
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action


from django import forms
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import UpdateView

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page



"""
課題
・fav_numを追加するのは更新（PUT？PATCH?）でデータを取得して上書きするスタイルで実装する
    ツイートidを取得してfav_numを+1,あるいは取り消しできるようにする
・ツイートフォームが二重になっているところは放置する
・ツイートフォームでいちいちuserとcreated_byを選ばないでいいように修正する
"""


class TweetsViewSet(viewsets.ModelViewSet):
    queryset = Tweet.objects.all()
    """
    tweetsのところに相当している
    postは全ユーザーでできるようになっている：あとで認証をかけることで解決できそう
        　どうやらここのpostメソッドが一番最初に読み込まれ、
        それがすべてのツイート可能ページに反映されるらしい。
        　したがって他のpostメソッドを改めて他のViewSetで記述する必要はない。
                もし記述してしまうと、ツイートフォームが二重になってしまう。
    """
    serializer_class = TweetSerializer
    print('\n'+'read inside TweetViewSet \n')
    def post(self, request, *args, **kwargs):
        print(7777777777777497)
        print(request.user.id)
        print(self.get_object().created_by.pk)
        if int(request.data.get("created_by")) != request.user.id:
            print(request.user.id)
            print(self.get_object().created_by.pk)
            raise PermissionDenied("You cannot create tweet with this user.")
        return super().create(request, *args, **kwargs)
    def destroy(self, request, *args, **kwargs):
        if self.get_object().created_by.pk != request.user.id:
            raise PermissionDenied("You cannot delete this tweet.")
        return super().destroy(request, *args, **kwargs)

    @action(methods=['get'], detail=True)
    def fav(self, request, pk):
        print(self.kwargs['pk'])
        tweet_id = self.kwargs['pk']
        print(tweet_id)
        tweet = Tweet.objects.get(id=tweet_id)
        print(tweet)
        is_fav = Fav.objects.filter(fav_user_id=self.request.user.id).filter(favtweet=tweet).count()
        print('is_fav:{}'.format(is_fav))
        # unfav
        if is_fav ==1:
            Fav.objects.get(favtweet=tweet,fav_user_id=self.request.user.id).delete()
            tweet.favs -= 1
            tweet.save()
        # fav
        else :
            Fav.objects.create(favtweet=tweet,fav_user=self.request.user)
            tweet.favs += 1
            tweet.save()

        return Response({'message':'fav succeeded!'})


class FavTweetView(UpdateView):
    fields = ('fav_num',)
    model = Tweet.objects.all()
    

