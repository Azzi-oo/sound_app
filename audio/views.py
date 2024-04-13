from rest_framework import generics, viewsets
from models import Genre, License
from oauth.permissions import IsAuthor
from serializers import GenreSerializer
from . import models, serializers


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
