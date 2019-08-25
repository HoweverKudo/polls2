from rest_framework import generics, status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Fav, Tweet
from .serializers import FavSerializer, TweetSerializer
from rest_framework.exceptions import PermissionDenied


class TweetViewSet(viewsets.ModelViewSet):
    queryset = Tweet.objects.all()
    """
    all_tweetsのところに相当している
    destroy：機能している
    postは全ユーザーでできるようになっている：あとで認証をかけることで解決できそう
    """
    serializer_class = TweetSerializer
    def post(self, request, *args, **kwargs):
        # print(self.kwargs["pk"])
        # print(request.data.get("created_by"))
        if str(self.kwargs["pk"]) != request.data.get("created_by"):
            raise PermissionDenied("You cannot create tweet with this user.")
        # print(request.data)
        return super().post(request, *args, **kwargs)
    def destroy(self, request, *args, **kwargs):
        if str(self.kwargs["pk"]) != request.data.get("created_by"):
            raise PermissionDenied("You cannot delete this tweet.")
        return super().destroy(request, *args, **kwargs)

# class PersonalTweetViewSet(viewsets.ModelViewSet):
#     """
#     同じユーザーに属するツイートを取り出す
#     """
#     serializer_class = TweetSerializer
#     """

#     """
#     def get_queryset(self):
#         queryset = Tweet.objects.filter(user_id=self.kwargs["pk"])
#         return queryset
#     def post(self, request, *args, **kwargs):
#         # print(self.kwargs["pk"])
#         # print(request.data.get("created_by"))
#         if   str(self.kwargs["pk"]) != request.data.get("created_by"):
#             raise PermissionDenied("You cannot create tweet with this user.")
#         # print(request.data.get("id"))
#         return super().post(request, *args, **kwargs)
#     def destroy(self, request, *args, **kwargs):
#         # print(self.kwargs["pk"])
#         # print(request.data.get("created_by"))
#         if str(self.kwargs["pk"]) != request.data.get("created_by"):
#             raise PermissionDenied("You cannot delete this tweet.")
#         return super().destroy(request, *args, **kwargs)

