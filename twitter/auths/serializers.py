from rest_framework import serializers
from polls.serializers import UserSerializer



class LoginSerializer(UserSerializer):

    class Meta(UserSerializer.Meta):
        fields = (
            *UserSerializer.Meta.fields,
        )
        read_only_fields = (
            *UserSerializer.Meta.read_only_fields,
        )


class LogoutSerializer(serializers.Serializer):
    """ログアウト専用シリアライザ 
    """
    pass