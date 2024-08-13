from rest_framework.exceptions import ValidationError

class ValidationImage:
    @staticmethod
    def validate(file):
        print(file)
        print(file.content_type)
        if not file:
            return
        if not file.content_type.startswith('image/'):
            raise ValidationError('el archivo debe ser una imagen')
