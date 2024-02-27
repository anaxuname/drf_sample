from rest_framework.serializers import ValidationError


class TitleValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        if not value.isalpha():
            raise ValidationError(self.field + " must contain only letters", value)
