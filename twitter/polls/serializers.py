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
    # follower_count = serializers.SerializerMethodField()
    # """
    # get_関数名()で関数に戻り値を引き渡すことができる
    # これにより、もとのモデルにはない属性をJSONデータとして表示させることができる
    # """
    # def get_follow_count(self, instance):
    #     return 100001
    # def get_follower_count(self, instance):
    #     return 8
    """
    どうにかしたいところ
    favs = serializers.SerializerMethodField()
    def get_favs(self, instance):
        n = instance.objects.all()[0].user.id
        return Tweet.objects.all()[n].user.favs
    """
    class Meta:
        model = CustumUser
        fields = ['username', 'email', 'password', 'id', 'follows', 'followers', 'profile']
        """
        passwordは書き込みしかできないようにする
        →createのreturn値からpassword, emailを除外する
        """
        extra_kwargs = {'password': {'write_only': True},
                            #'email': {'write_only': True},
                            'follows': {'read_only': True},
                            'followers': {'read_only': True},
                            'favs': {'read_only': True}}

    def create(self, validated_data):
        """
        createメソッドをoverrideする
        validated_dataのうち、email, usernameをCustumUserモデルに引き渡す
        """
        print(validated_data)
        user = CustumUser(
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