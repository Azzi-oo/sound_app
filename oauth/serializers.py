from rest_framework import serializers
from . import models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AuthUser
        fields = ('avatar', 'country', 'city', 'bio', 'display_name')


class SociallinkSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.Sociallink
        fields = ('id', 'link',)


class AuthorSerializer(serializers.ModelSerializer):
    social_links = SociallinkSerializer(many=True)

    class Meta:
        model = models.AuthUser
        fields = ('id', 'avatar', 'country', 'city', 'bio', 'display_name')


class GoogleAuth(serializers.Serializer):
    email = serializers.EmailField()
    token = serializers.CharField()
