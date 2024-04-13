from rest_framework import viewsets, parsers, permissions
from oauth.serializers import UserSerializer, AuthorSerializer, SociallinkSerializer
from oauth.models import AuthUser
from oauth.permissions import IsAuthor


class UserView(viewsets.ModelViewSet):
    parser_classes = (parsers.MultiPartParser,)
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user

    def get_object(self):
        return self.get_queryset()


class AuthorView(viewsets.ReadOnlyModelViewSet):
    queryset = AuthUser.objects.all().prefetch_related('social_links')
    serializer_class = AuthorSerializer


class SocialLinkView(viewsets.ModelViewSet):
    serializer_class = SociallinkSerializer
    permission_classes = [IsAuthor]

    def get_queryset(self):
        return self.request.user.social_links.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
