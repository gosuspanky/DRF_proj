from rest_framework.serializers import ValidationError

allowed_link = "www.youtube.com"


def validate_link(value):
    """
    Проверка ссылки на видео

    :param value: вводимая ссылка
    :raise ValidationError: Выводит ошибку, если ссылка не соответствует требованиям
    """
    if allowed_link not in value.split("/"):
        raise ValidationError(
            "Ссылка должна быть на видео с сайта Youtube и начинаться с www.youtube.com"
        )
