from rest_framework import serializers
from .models import Tweet, Fav




class FavSerializer(serializers.ModelDurationField):
    class Meta:
        model = Fav
        fields = '__all__'

class TweetSerializer(serializers.ModelSerializer):

    # fvs = serializers.SerializerMethodField()
    # def get_fvs(self, instance):
    #     tw = instance.objects.all()[0]
    #     t = tw.user.favs
    #     return t

    class Meta:
        """
        もしかしたらfieldsは__all__だとまずいかもしれない
        """
        model = Tweet
        fields = ['user', 'body', 'created_at', 'created_by', 'favs']
        extra_kwargs = {'favs': {'read_only': True}}
        
    