from django.core.exceptions import ValidationError


def get_path_upload_avatar():
    return f"avatar/{instance.id}/{file}"


def validate_size_image(file_obj):
    megabite_limit = 2
    if file_obj.size > megabite_limit * 1024 * 1024:
        raise ValidationError("Максимальный размер файла {megabite_limit}MB")
    