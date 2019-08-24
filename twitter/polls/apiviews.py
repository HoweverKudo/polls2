from rest_framework import generics, status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Poll, Choice
from .serializers import PollSerializer, ChoiceSerializer, VoteSerializer, UserSerializer

from django.contrib.auth import authenticate
from rest_framework.exceptions import PermissionDenied

# class PollList(APIView):
#     def get(self, request):
#         polls = Poll.objects.all()[:20]
#         data = PollSerializer(polls, many=True).data
#         return Response(data)


# class PollDetail(APIView):
#     def get(self, request, pk):
#         poll = get_object_or_404(Poll, pk=pk)
#         data = PollSerializer(poll).data
#         return Response(data)


# class PollList(generics.ListCreateAPIView):
#     """
#     genericsのクラスを継承して、Pollモデルを関係付けることで
#     リストのクラスを簡単に作成できる
#     """    
#     queryset = Poll.objects.all()
#     serializer_class = PollSerializer

# class PollDetail(generics.RetrieveDestroyAPIView):
#     """
#     genericsのクラスを継承して、Pollモデルを関係付けることで
#     詳細データのクラスを簡単に作成できる
#     """  
#     queryset = Poll.objects.all()
#     serializer_class = PollSerializer

class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

    def destroy(self, request, *args, **kwargs):
        poll = Poll.objects.get(pk=self.kwargs["pk"])
        if not request.user == poll.created_by:
            raise PermissionDenied("You cannot delete this poll.")
        return super().destroy(request, *args, **kwargs)
    

# class ChoiceList(generics.ListCreateAPIView):
#     queryset = Choice.objects.all()
#     serializer_class = ChoiceSerializer

# class CreateVote(generics.CreateAPIView):
#     serializer_class = VoteSerializer

class ChoiceList(generics.ListCreateAPIView):
    """
    同じ質問に属する選択肢を取り出す
    適切なrestを作るためにネストしていく
    get_querysetメソッドをoverrideする
    """
    def get_queryset(self):
        queryset = Choice.objects.filter(poll_id=self.kwargs["pk"])
        return queryset
    serializer_class = ChoiceSerializer

    def post(self, request, *args, **kwargs):
        poll = Poll.objects.get(pk=self.kwargs["pk"])
        if not request.user == poll.created_by:
            raise PermissionDenied("You cannot create choice for this poll.")
        return super().post(request, *args, **kwargs)


class CreateVote(APIView):
    serializer_class = VoteSerializer
    """
    choice_pkを受け取ってからuketottekaravoteさせるようにする
    こうすることでvoteを<choice_pk>の下の階層にネストできる
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