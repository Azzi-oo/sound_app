from rest_framework import serializers
from . import models
from ..oauth.serializers import AuthorSerializer


class BaseSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Genre
        fields = ('id', 'name')


class LicenseSerializer(BaseSerializer):
    class Meta:
        model = models.License
        fields = ('id', 'text')


class CreateAuthorTrackSerializer(BaseSerializer):
    plays_count = serializers.IntegerField(read_only=True)
    download = serializers.IntegerField(read_only=True)
    user = serializers.IntegerField(read_oanly=True)

    class Meta:
        model = models.Track
        fields = (
            'id',
            'title',
            'license',
            'genre',
            'album',
            'link_of_author',
            'file',
            'create_at',
            'plays_count',
            'download',
            'private',
            'cover',
            'user',
        )

    def update(self, instance, validated_data):
        delete_old_file(instance.file.path)
        delete_old_file(instance.cover.path)
        return super().update(instance, validated_data)


class AuthorTrackSerializer(CreateAuthorTrackSerializer):
    license = LicenseSerializer()
    genre = GenreSerializer(many=True)
    album = AlbumSerializer()
    user = AuthorSerializer()


class CreatePlayListSerializer(BaseSerializer):
    class Meta:
        model = models.PlayList
        fields = ('id', 'title', 'cover', 'track')

    def update(self, instance, validated_data):
        delete_old_file(instance.cover.path)
        return super().update(instance, validated_data)


class PlayListSerializer(CreatePlayListSerializer):
    track = AuthorTrackSerializer(many=True)


class CommentAuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Comment
        fields = ('id', 'text', 'track')
