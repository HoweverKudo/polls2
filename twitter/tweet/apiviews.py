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
        """
        頼むから読んでくれ
        """
        print(self.kwargs["pk"])
        print(request.data.get("created_by"))
        if str(self.kwargs["pk"]) != request.data.get("created_by"):
            raise PermissionDenied("You cannot create tweet with this user.")
        return super().post(request, *args, **kwargs)
    def destroy(self, request, *args, **kwargs):
        if self.get_object().created_by.pk != request.user.id:
            raise PermissionDenied("You cannot delete this tweet.")
        return super().destroy(request, *args, **kwargs)

class PersonalPageViewSet(viewsets.ModelViewSet):
    """
    同じユーザーに属するツイートを取り出す
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
        print("pass")
        #if self.get_object().created_by.pk != request.user.id:
        if str(self.kwargs["pk"]) != request.data.get("created_by"):
            raise PermissionDenied("You cannot create tweet with this user.")
        return self.create(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        print()
        print(type(self.kwargs["pk"]))
        print(request.data.get("created_by"))
        print(User.objects.all())
        print(dir(request.user.username))
        print(request.user)
        print()
        if int(self.kwargs["pk"]) != request.user.id:
            raise PermissionDenied("You cannot delete this tweet!.")
        return self.destroy(request, *args, **kwargs)
    
    @action(methods=['get'], detail=True)
    def profile(self, request, pk=None):
        tweet = Tweet.objects.filter(user_id=self.kwargs["pk"])
        data = TweetSerializer(tweet, many=True).data
        return Response(data=data)
