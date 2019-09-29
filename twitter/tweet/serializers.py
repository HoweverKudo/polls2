from rest_framework import serializers
from .models import Tweet, Fav




class FavSerializer(serializers.ModelDurationField):
    class Meta:
        model = Fav
        fields = '__all__'

class TweetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tweet
        fields = ['id', 'user', 'body', 'created_at', 'created_by', 'favs']
        extra_kwargs = {'favs': {'read_only': True}}
        
    