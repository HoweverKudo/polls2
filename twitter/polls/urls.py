from django.urls import path
from .apiviews import PollViewSet, ChoiceList, CreateVote, UserCreate, LoginView, UserList
from tweet.apiviews import TweetViewSet, PersonalTweetViewSet
from rest_framework.routers import DefaultRouter

from rest_framework.authtoken import views

"""
PollViewSetをpollsという名前でrouterにregisterする
routerで登録するのは一箇所のurls.pyにまとめて書かないと読み込んでくれない仕様になっているので注意
"""
router = DefaultRouter()
router.register('polls', PollViewSet, base_name='polls')
router.register('all_tweets', TweetViewSet, base_name='tweets')



urlpatterns = [
    # クラスとして記述したものをビューに変換して受け取れるようにするのがas_view()メソッド
    path("polls/<int:pk>/choices/", ChoiceList.as_view(), name="choices_list"),
    path("polls/<int:pk>/choices/<int:choice_pk>/vote/", CreateVote.as_view(), name="create_vote"),
    path("signup/", UserCreate.as_view(), name="user_create"),
    path("login/", LoginView.as_view(), name="login"),
    path("all_tweets/users/", UserList.as_view(), name="user_list"),
]

urlpatterns += router.urls