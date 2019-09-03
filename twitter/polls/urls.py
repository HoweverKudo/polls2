from django.urls import path, include
from django.contrib import admin
from django.conf.urls import url
from .apiviews import PollViewSet, ChoiceList, CreateVote, UserCreate, UserList, UserViewSet, LogoutView
from tweet.apiviews import TweetsViewSet, FavTweetView
from rest_framework.routers import DefaultRouter, SimpleRouter
#from rest_framework.authtoken import views
from rest_framework.schemas import get_schema_view

schema_view = get_schema_view(title='Twitter API')


"""
PollViewSetをpollsという名前でrouterにregisterする
routerで登録するのは一箇所のurls.pyにまとめて書かないと読み込んでくれない仕様になっているので注意
"""
# router = DefaultRouter()

# router.register('polls', PollViewSet, base_name='polls')
# router.register('all_tweets', TweetViewSet, base_name='all_tweets')
# router.register('all_tweets/users', PersonalPageViewSet, base_name='personal_page')

router = SimpleRouter()
router.register('users', UserViewSet, base_name='users')
router.register('tweets', TweetsViewSet, base_name='tweets')

urlpatterns = [
    path('admin/', admin.site.urls),
    # クラスとして記述したものをビューに変換して受け取れるようにするのがas_view()メソッド
    path("polls/<int:pk>/choices/", ChoiceList.as_view(), name="choices_list"),
    path("polls/<int:pk>/choices/<int:choice_pk>/vote/", CreateVote.as_view(), name="create_vote"),


    # 自作のlogin, logout
    # path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name='logout'),


    # 提供されているlogin, logout　
    # しかし、UserViewSetで作ったuserでのログインとは別のログインになってしまっている
    # さらに、password/reset/までも提供されている
    # path("twitter/v1/rest_auth/", include('rest_auth.urls')),
    # path("", include('rest_auth.urls')),
    # path('accounts/', include('allauth.urls')),



    # url('api-token-auth/', views.obtain_auth_token),

    # 自作（前者）、提供（後者）
    # path("twitter/v1/rest_auth/registration/", include('rest_auth.registration.urls')),
    # path("signup/", UserCreate.as_view(), name="user_create"),

    # favAPI
    path('tweets/<int:pk>/fav', FavTweetView.as_view(), name='fav'),
    
    path('schema/', schema_view),
]

urlpatterns += router.urls