from django.contrib.auth import authenticate
from django.contrib.auth import login as _login
from django.contrib.auth import logout as _logout
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from polls.serializers import UserSerializer
from auths.serializers import LoginSerializer, LogoutSerializer

class AuthViewSets(viewsets.GenericViewSet): 
    """Auth API
    """

    def get_serializer_class(self):
        _action = self.action
        serializer_class = UserSerializer

        if _action == 'login':
            serializer_class = LoginSerializer
        elif _action == 'logout':
            serializer_class = LogoutSerializer
        elif _action == 'me':
            serializer_class = UserSerializer

        return serializer_class

    @action(
        detail=False,
        methods=['post'],
        permission_classes=[AllowAny]
    )
    def login(self, request):
        """ログイン API
        """
        print("hello")
        # リクエスト内容をバリデート
        # validation_serializer = self.get_serializer(
        #     data=request.data, context={'request': request}
        # )
        # validation_serializer.is_valid(raise_exception=True)

        
        user: 'polls.models.CustumUser' = authenticate(
            request,
            username=request.data['username'],  
            password=request.data['password']
        )
        
        if user is None:
            print(request.data.get('password'))
            print(request.data["username"])
            return Response(status=status.HTTP_400_BAD_REQUEST)
        _login(request, user)

        serializer = self.get_serializer(user, context={'request': request})

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=['post'],
    )
    def logout(self, request):
        """ログアウト API
        """
        _logout(request)
        serializer = self.get_serializer(
            data=request.data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    @action(
        detail=False,
        methods=['get'],
    )
    def me(self, request):
        """me API
        """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
