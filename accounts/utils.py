import uuid

from django.core.exceptions import ValidationError


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    ext = filename.split('.')[-1]
    filename_rename = f'{uuid.uuid4()}.{ext}'
    return '{0}/user_{1}/{2}'.format(
        instance.user.id, str(instance.__class__.__name__).lower(), filename_rename
    )


def validate_file_size(value):
    filesize = value.size
    if filesize > 3670016:
        raise ValidationError("The maximum image size that can be uploaded is 3.5MB.")
    else:
        return value
