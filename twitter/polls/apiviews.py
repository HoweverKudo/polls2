from rest_framework import generics, status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Poll, Choice
from .serializers import PollSerializer, ChoiceSerializer, VoteSerializer, UserSerializer
from .models import CustumUser

from django.contrib.auth import authenticate, logout
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.authentication import SessionAuthentication, BasicAuthentication


class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer
    """
    ViewSetにはlist, create, retrieve, destroyがまとめて入っている
    destroyメソッドをoverride
    """
    def destroy(self, request, *args, **kwargs):
        poll = Poll.objects.get(pk=self.kwargs["pk"])
        if not request.user == poll.created_by:
            raise PermissionDenied("You cannot delete this poll.")
        return super().destroy(request, *args, **kwargs)
    

class ChoiceList(generics.ListCreateAPIView):
    """
    同じ質問に属する選択肢を取り出す
    適切なrestを作るためにネストしていく
    get_querysetメソッドをoverrideする
    """
    serializer_class = ChoiceSerializer

    def get_queryset(self):
        queryset = Choice.objects.filter(poll_id=self.kwargs["pk"])
        return queryset
    def post(self, request, *args, **kwargs):
        poll = Poll.objects.get(pk=self.kwargs["pk"])
        if not request.user == poll.created_by:
            raise PermissionDenied("You cannot create choice for this poll.")
        return super().post(request, *args, **kwargs)


class CreateVote(APIView):
    serializer_class = VoteSerializer
    """
    choice_pkを受け取ってからvoteさせるようにする
    こうすることでvoteを<choice_pk>の下の階層にネストできる
    postメソッドをoverride
    """
    def post(self, request, pk, choice_pk):
        voted_by = request.data.get("voted_by")
        data = {'choice': choice_pk, 'poll': pk, 'voted_by': voted_by}
        serializer = VoteSerializer(data=data)
        if serializer.is_valid():
            vote = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserCreate(generics.CreateAPIView):
    """
    ユーザー作成には無条件で権限を与えておく
    そうしないとユーザーが作れないため
    下のように記述してグローバルauthentication schemeをoverrideする
    """
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer

class UserList(generics.ListAPIView):
    """
    Listだけ表示したいならListAPIViewを用いる
    """
    queryset = CustumUser.objects.all().select_related()
    serializer_class = UserSerializer 
    def list(self, request):
        data = UserSerializer(CustumUser.objects.select_related(), many=True).data
        return Response(status=200, data=data)
    
class UserViewSet(viewsets.ModelViewSet):
    queryset = CustumUser.objects.all()
    serializer_class = UserSerializer

    @action(methods=['get'], detail=True)
    def follow(self, request, pk):
        """
        following, followers はmanytomanyfieldで実装
        フォロー・フォロワー数はmodelsの関数で定義する
        """
        followuser = CustumUser.objects.all().get(username=request.user)
        followed_user_id = int(self.kwargs['pk'])
        """
        フォロー・フォロワーを追加
        """
        CustumUser.objects.all().filter(id=followed_user_id)[0].followers.add(followuser.id)
        CustumUser.objects.all().filter(id=followuser.id)[0].following.add(followed_user_id)
        return Response({'message':'follow succeeded!'})

    @action(methods=['get'], detail=True)
    def unfollow(self, request, pk):
        """
        following, followers はmanytomanyfieldで実装
        フォロー・フォロワー数はmodelsの関数で定義する
        """
        unfollowuser = CustumUser.objects.all().get(username=request.user)
        unfollowed_user_id = int(self.kwargs['pk'])
        """
        フォロー・フォロワーを追加
        """
        CustumUser.objects.all().filter(id=unfollowed_user_id)[0].followers.remove(unfollowuser.id)
        CustumUser.objects.all().filter(id=unfollowuser.id)[0].following.remove(unfollowed_user_id)
        return Response({'message':'unfollow succeeded!'})
    
    


class LoginView(APIView):
    permission_classes = ()

    def post(self, request, format=None):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        print(user)
        if user:
            return Response({"message": "Login Succeeded"})
        else:
            return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)
"""
class LogoutView(APIView):
    permission_classes = ()

    def post(self, request):
        logout(request)
        return Response({"message": "logged out"}, status=status.HTTP_202_ACCEPTED)

"""
class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response()