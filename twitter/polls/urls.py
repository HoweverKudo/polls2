from django.urls import path, include
from django.contrib import admin
from django.conf.urls import url
from .apiviews import PollViewSet, ChoiceList, CreateVote, UserCreate, UserList, UserViewSet, LoginView,LogoutView
from tweet.apiviews import TweetsViewSet, FavTweetView
from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework_jwt.views import obtain_jwt_token
from auths.apiviews import AuthViewSets
from rest_framework.schemas import get_schema_view

schema_view = get_schema_view(title='Twitter API')


"""
PollViewSetをpollsという名前でrouterにregisterする
routerで登録するのは一箇所のurls.pyにまとめて書かないと読み込んでくれない仕様になっているので注意
"""


router = SimpleRouter()
router.register('users', UserViewSet, base_name='users')
router.register('tweets', TweetsViewSet, base_name='tweets')

# router.register('', AuthViewSets, base_name='auth')

urlpatterns = [
    path('admin/', admin.site.urls),
    # クラスとして記述したものをビューに変換して受け取れるようにするのがas_view()メソッド
    path("polls/<int:pk>/choices/", ChoiceList.as_view(), name="choices_list"),
    path("polls/<int:pk>/choices/<int:choice_pk>/vote/", CreateVote.as_view(), name="create_vote"),


    # 自作のlogin, logout
    # path("login/", LoginView.as_view(), name="login"),
    # path("logout/", LogoutView.as_view(), name='logout'),
    path('', include('rest_auth.urls')),
    # path('registration/', include('rest_auth.registration.urls')),


    # 提供されているlogin, logout　
    # url("login/", obtain_jwt_token),


    # favAPI
    path('tweets/<int:pk>/fav', FavTweetView.as_view(), name='fav'),
    
    path('schema/', schema_view),
]

urlpatterns += router.urls