from rest_framework import serializers
from .models import Tweet, Fav
from django.contrib.auth.models import User



class FavSerializer(serializers.ModelDurationField):
    class Meta:
        model = Fav
        fields = '__all__'

class TweetSerializer(serializers.ModelSerializer):
    #fav = FavSerializer()
    class Meta:
        """
        もしかしたらfieldsは__all__だとまずいかもしれない
        """
        model = Tweet
        fields = '__all__'