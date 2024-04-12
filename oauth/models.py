from django.db import models
from django.core.validators import FileExtensionValidator

from base.services import get_path_upload_avatar, validate_size_image


class AuthUser(models.Model):
    email = models.EmailField(max_length=150, unique=True)
    join_date = models.DateTimeField(auto_now_add=True)
    country = models.CharField(max_length=30, blank=True, null=True)
    bio = models.TextField()
    display_name = models.CharField(max_length=30, blank=True, null=True)
    avatar = models.ImageField(
        upload_to=get_path_upload_avatar,
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg']), validate_size_image]
    )

    @property
    def is_authenticated(self):
        return True

    def __str__(self) -> str:
        return self.email


class Follower(models.Model):
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name='owner')
    subscriber = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name='subscribers')

    def __str__(self) -> str:
        return f'{self.subscriber} подписан на {self.user}'


class Sociallink(models.Model):
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name='social_link')
    link = models.URLField(max_length=100)

    def __str__(self) -> str:
        return f'{self.user}'
