from rest_framework import generics, status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Fav, Tweet
from .serializers import FavSerializer, TweetSerializer
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django import forms
from django.shortcuts import redirect
from django.views.generic import UpdateView


"""
課題
・fav_numを追加するのは更新（PUT？PATCH?）でデータを取得して上書きするスタイルで実装する
    ツイートidを取得してfav_numを+1,あるいは取り消しできるようにする
・ツイートフォームが二重になっているところは放置する
・ログアウトのエンドポイントを実装し、
    ツイートフォームでいちいちuserとcreated_byを選ばないでいいように修正する
"""


class TweetsViewSet(viewsets.ModelViewSet):
    queryset = Tweet.objects.all()
    """
    tweetsのところに相当している
    destroy：login中のユーザーしか削除できなくできた！
    postは全ユーザーでできるようになっている：あとで認証をかけることで解決できそう
        　どうやらここのpostメソッドが一番最初に読み込まれ、
        それがすべてのツイート可能ページに反映されるらしい。
        　したがって他のpostメソッドを改めて他のViewSetで記述する必要はない。
                もし記述してしまうと、ツイートフォームが二重になってしまう。
    """
    serializer_class = TweetSerializer
    print(77779)
    def post(self, request, *args, **kwargs):
        if int(request.data.get("created_by")) != request.user.id:
            raise PermissionDenied("You cannot create tweet with this user.")
        return super().post(request, *args, **kwargs)
    def destroy(self, request, *args, **kwargs):
        if self.get_object().created_by.pk != request.user.id:
            raise PermissionDenied("You cannot delete this tweet.")
        return super().destroy(request, *args, **kwargs)

# class TweetsViewSet(viewsets.ModelViewSet):
#     """
#     個人のツイート履歴はurlにprofile/を追加して見れます
#     例：http://0.0.0.0:8040/tweets/1/profile/
#     """
#     serializer_class = TweetSerializer
    
    # def get_queryset(self):
    #     queryset = Tweet.objects.filter(user_id=self.kwargs.get("pk"))
    #     return queryset
    
    # def post(self, request, *args, **kwargs):
    #     print(800000000)
    #     """
    #     self.create(〜)でpostが反映されるようになった
    #     """
    #     if int(request.data.get("created_by")) != request.user.id:
    #         raise PermissionDenied("You cannot create tweet with this user.")
    #     return self.create(request, *args, **kwargs)

    # def destroy(self, request, *args, **kwargs):
    #     """
    #     profile pageを削除するメソッド
    #     delete_tweetメソッドを呼び出すとツイート回数分だけ呼び出されてしまう
    #     """
    #     if int(self.kwargs["pk"]) != request.user.id:
    #         raise PermissionDenied("You cannot delete this profile page.")
    #     return self.destroy(request, *args, **kwargs)

    # def list(self, request, pk=None):
    #     tweets = Tweet.objects.filter(id=self.kwargs["pk"])
    #     print(tweets[0])
    #     data = TweetSerializer(tweets, many=True).data
    #     return Response(data=data)

    # @action(methods=['get'], detail=True)
    # def profile(self, request, pk=None):
    #     tweets = Tweet.objects.filter(user_id=self.kwargs["pk"])
    #     print(tweets[0])
    #     data = TweetSerializer(tweets, many=True).data
    #     return Response(data=data)
    # @action(methods=['get'], detail=True)
    # def delete_tweet(self, request, pk, **kwargs):
    #     print(request.data.get("created_by"))
    #     print(Tweet.objects.filter(user_id=self.kwargs["pk"])[0])
    #     print(self.kwargs["pk"])
        
    #     # print(self.id)
    #     print(Tweet.objects.filter(user_id=self.kwargs["pk"]))
    #     tweets = Tweet.objects.filter(user_id=self.kwargs["pk"])
    #     if int(self.kwargs["pk"]) != request.user.id:
    #         raise PermissionDenied("You cannot delete this tweet!.")
    #     return ?
        
class FavTweetView(UpdateView):
    fields = ('fav_num',)
    model = Tweet.objects.all()
    
# class FavTweet(generics.UpdateAPIView):
#     queryset = Tweet.objects.all()
#     serializer_class = TweetSerializer
#     permission_classes = (IsAuthenticated,)
#     def update(self, instance, validated_data):
#         instance = self.get_object()
#         print(dir(instance))
#         instance.save()
#         return instance

# @login_required
# def fav(self, instance,):
#     tweet = Tweet.objects.get(id=tweet_id)
#     is_fav = Fav.objects.filter(fav_user_id=request.user.id).filter(favtweet=tweet).count()

#     # unfav
#     if is_fav >0:
#         # Fav.objects.get(favtweet=tweet,fav_user_id=request.user.id).delete()
#         tweet.fav_num -= 1
#         tweet.save()
#     # fav
#     else :
#         # Fav.objects.create(favtweet=tweet,fav_user=request.user)
#         tweet.fav_num += 1
#         tweet.save()
    
#     return redirect('/tweets/<int:pk>')
