from django.urls import path
from .apiviews import PollViewSet, ChoiceList, CreateVote, UserCreate, LoginView
from rest_framework.routers import DefaultRouter

from rest_framework.authtoken import views




"""
PollViewSetをpollsという名前でrouterにregisterする
"""
router = DefaultRouter()
router.register('polls', PollViewSet, base_name='polls')

urlpatterns = [
    # クラスとして記述したものをビューに変換して受け取れるようにするのがas_view()メソッド
    path("polls/<int:pk>/choices/", ChoiceList.as_view(), name="choices_list"),
    path("polls/<int:pk>/choices/<int:choice_pk>/vote/", CreateVote.as_view(), name="create_vote"),
    path("users/", UserCreate.as_view(), name="user_create"),
    path("login/", LoginView.as_view(), name="login"),
]

urlpatterns += router.urls