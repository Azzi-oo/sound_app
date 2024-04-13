from django.core.exceptions import ValidationError


def get_path_upload_avatar(instance, file):
    return f"avatar/{instance.id}/{file}"


def get_path_upload_cover_album(instance, file):
    return f"avatar/user_{instance.id}/{file}"


def get_path_upload_cover_playlist(instance, file):
    return f"playlist/user_{instance.id}/{file}"


def get_path_upload_track(instance, file):
    return f"track/user_{instance.id}/{file}"


def validate_size_image(file_obj):
    megabite_limit = 2
    if file_obj.size > megabite_limit * 1024 * 1024:
        raise ValidationError("Максимальный размер файла {megabite_limit}MB")
