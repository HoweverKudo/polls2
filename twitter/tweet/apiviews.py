from rest_framework import generics, status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Fav, Tweet
from .serializers import FavSerializer, TweetSerializer
from rest_framework.exceptions import PermissionDenied

from rest_framework.decorators import action
from django.contrib.auth.models import User
from django import forms


class TweetViewSet(viewsets.ModelViewSet):
    queryset = Tweet.objects.all()
    """
    all_tweetsのところに相当している
    destroy：login中のユーザーしか削除できなくできた！
    postは全ユーザーでできるようになっている：あとで認証をかけることで解決できそう
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

class PersonalPageViewSet(viewsets.ModelViewSet):
    """
    個人のツイート履歴はurlにprofile/を追加して見れます
    例：http://0.0.0.0:8040/all_tweets/users/1/profile/
    """
    serializer_class = TweetSerializer

    """
    例えば、user_idが１の人のツイートを
    全部見れ(list)、削除でき(destroy)、追加できる(post)
    エンドポイントをつくりたい
    """
    def get_queryset(self):
        queryset = Tweet.objects.filter(user_id=self.kwargs["pk"])
        return queryset

    def post(self, request, *args, **kwargs):
        """
        self.create(〜)でpostが反映されるようになった
        """
        if int(request.data.get("created_by")) != request.user.id:
            raise PermissionDenied("You cannot create tweet with this user.")
        return self.create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        profile pageを削除するメソッド
        delete_tweetメソッドを呼び出すとツイート回数分だけ呼び出されてしまう
        """
        print()
        print(type(self.kwargs["pk"]))
        print(request.data.get("created_by"))
        print(User.objects.all())
        print(dir(request.user.username))
        print(request.user)
        print()
        # if int(request.data.get("created_by")) != request.user.id:
        if int(self.kwargs["pk"]) != request.user.id:
            raise PermissionDenied("You cannot delete this profile page.")
        return self.destroy(request, *args, **kwargs)

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
        
    
    @action(methods=['get'], detail=True)
    def profile(self, request, pk=None):
        tweets = Tweet.objects.filter(user_id=self.kwargs["pk"])
        print(tweets[0])
        data = TweetSerializer(tweets, many=True).data
        return Response(data=data)
