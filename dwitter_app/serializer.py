from rest_framework import serializers
from .models import *

class DweetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dweets
        fields = '__all__'


class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'


class FollowersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Followers
        fields = '__all__'