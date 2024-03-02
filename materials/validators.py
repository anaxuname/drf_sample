from rest_framework.serializers import ValidationError

RIGHT_LINK = "https://www.youtube.com"


class LinkValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        if not value.startswith(RIGHT_LINK):
            raise ValidationError("Wrong link")
