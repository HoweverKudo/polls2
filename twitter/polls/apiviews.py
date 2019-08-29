from rest_framework import generics, status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Poll, Choice
from .serializers import PollSerializer, ChoiceSerializer, VoteSerializer, UserSerializer
from .models import User

from django.contrib.auth import authenticate
from rest_framework.exceptions import PermissionDenied

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
    queryset = User.objects.all().select_related()
    serializer_class = UserSerializer 
    def list(self, request):
        data = UserSerializer(User.objects.select_related(), many=True).data
        return Response(status=200, data=data)
    
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class LoginView(APIView):
    permission_classes = ()

    def post(self, request, format=None):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            return Response({"token": user.auth_token.key})
        else:
            return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)