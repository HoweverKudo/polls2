from django.urls import path, include
from django.contrib import admin
from django.conf.urls import url

from .apiviews import (
    UserCreate, 
    UserViewSet, 
)
from tweet.apiviews import (
    TweetsViewSet, 
    FavTweetView
)
from auths.apiviews import AuthViewSets

from rest_framework.routers import SimpleRouter
from rest_framework.schemas import get_schema_view

from twitter.cache import cache_page

schema_view = get_schema_view(title='Twitter API')

"""
PollViewSetをpollsという名前でrouterにregisterする
routerで登録するのは一箇所のurls.pyにまとめて書かないと読み込んでくれない仕様になっているので注意
"""

router = SimpleRouter()
router.register('users', UserViewSet, base_name='users')
router.register('tweets', TweetsViewSet, base_name='tweets')
router.register('', AuthViewSets, base_name='auth')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tweets/<int:pk>/fav', FavTweetView.as_view(), name='fav'),
    path('schema/', schema_view),
]

urlpatterns += router.urls