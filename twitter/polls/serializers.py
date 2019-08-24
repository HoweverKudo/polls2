from rest_framework import serializers

from .models import Poll, Choice, Vote
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = '__all__'

class ChoiceSerializer(serializers.ModelSerializer):
    votes = VoteSerializer(many=True, required=False)

    class Meta:
        model = Choice
        fields = '__all__'

class PollSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True, required=False)

    class Meta:
        model = Poll
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        """
        passwordは書き込みしかできないようにする
        →createのreturn値からpasswordを除外する
        """
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        """
        createメソッドをoverrideする
        validated_dataのうち、email, usernameをUserモデルに引き渡す
        """
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        """
        Userモデルから作ったuserデータのpasswordは、validated_dataのpasswordにする
        """
        user.set_password(validated_data['password'])
        user.save()
        """
        token認証を追加する
        ユーザー作成時にtokenもつくる
        """
        Token.objects.create(user=user)
        return user