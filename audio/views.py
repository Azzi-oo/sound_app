import os
from django import views
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets, parsers
from models import Genre, License
from oauth.permissions import IsAuthor
from serializers import GenreSerializer
from . import models, serializers
from django_filters.rest_framework import DjangoFilterBackend


class GenreView(generics.ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class LicenseView(viewsets.ModelViewSet):
    serializer_class = serializers.LicenseSerializer
    permission_classes = [IsAuthor]

    def get_queryset(self):
        return License.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TrackView(MixedSerializer, viewsets.ModelViewSet):
    parser_classes = (parsers.MultiPartParser,)
    permission_classes = [IsAuthor]
    serializer_class = serializers.CreateAuthorTrackSerializer
    serializer_classes_by_action = {
        'list': serializers.AuthorTrackSerializer
    }

    def get_queryset(self):
        return models.Track.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance):
        delete_old_file(instance.cover.path)
        delete_old_file(instance.file.path)
        instance.delete()


class TrackListView(generics.ListAPIView):
    queryset = models.Track.objects.filter(album__private=False, private=False)
    serializer_class = serializers.AuthorTrackSerializer
    pagination_class = Pagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'user__display_name', 'album__name', 'genre__name']


class AuthorTrackListView(generics.ListAPIView):
    serializer_class = serializers.AuthorTrackSerializer
    pagination_class = Pagination

    def get_queryset(self):
        return models.Track.objects.filter(user__id=self.kwargs.get('pk'), album__private=False, private=False)


class CommentAuthorView(viewsets.ModelViewSet):
    serializer_class = serializers.CommentAuthorSerializer
    permission_classes = [IsAuthor]

    def get_queryset(self):
        return models.Comment.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentView(viewsets.ModelViewSet):
    serializer_class = serializers.CommentSerializer

    def get_queryset(self):
        return models.Comment.objects.filter(track_id=self.kwargs.get('pk'))
    

class StreamingFileView(views.APIView):
    def set_play(self):
        self.track.plays_count += 1
        self.track.save()

    def get(self, request, pk):
        self.track = get_object_or_404(models.Track, id=pk, private=False)
        if os.path.exists(self.track.file.path):
            self.set_play()
            response = HttpResponse('', content_type='audio/mpeg', status=206)
            response['X-Accel-Redirect'] = f"/mp3/{self.track.file.name}"
            return response
        else:
            return Http404


class StreamingFileAuthorView(views.APIView):
    permission_classes = [IsAuthor]

    def get(self, request, pk):
        self.track = get_object_or_404(models.Track, id=pk, user=request.user)
        if os.path.exists(self.track.file.path):
            response = HttpResponse('', content_type="audio/mpeg", status=206)
            response['X-Accel-Redirect'] = f"/mp3/{self.track.file.name}"
            return response
        else:
            return Http404
