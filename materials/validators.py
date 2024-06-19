from rest_framework.serializers import ValidationError

allowed_link = "www.youtube.com"


def validate_link(value):
    if allowed_link not in value.split("/"):
        raise ValidationError(
            "Ссылка должна быть на видео с сайта Yutube и начинаться с www.youtube.com"
        )
