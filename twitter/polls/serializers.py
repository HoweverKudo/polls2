from rest_framework import serializers

from .models import Poll, Choice, Vote
from .models import CustumUser
from tweet.models import Tweet
from rest_framework.authtoken.models import Token

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = '__all__'

class ChoiceSerializer(serializers.ModelSerializer):
    """
    many=Trueでデータがlist形式になる場合も処理できるようになる
    """
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
    # """
    # シリアライザーのところでserializers.SerializerMethodField()を用いることで、
    # 新たなメソッドを定義できる
    # """
    # follow_count = serializers.SerializerMethodField()
    # """
    # get_関数名()で関数に戻り値を引き渡すことができる
    # これにより、もとのモデルにはない属性をJSONデータとして表示させることができる
    # """
    # def get_follow_count(self, instance):
    #     return 100001
    class Meta:
        model = CustumUser
        fields = ['username', 'email', 'password', 'id', 'follow_num', 'follower_num', 'following', 'followers', 'profile']
        """
        passwordは書き込みしかできないようにする
        →createのreturn値からpassword, emailを除外する
        """
        read_only_fields = (
            'follow_num',
            'follower_num',
            'following',
            'followers',
            'favs',
        )
        extra_kwargs = {'password': {'write_only': True},
                            }
