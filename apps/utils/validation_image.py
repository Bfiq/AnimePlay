from rest_framework.exceptions import ValidationError

class ValidationFiles:
    @staticmethod
    def validate_image(file):
        print(file)
        print(file.content_type)
        if not file:
            return
        if not file.content_type.startswith('image/'):
            raise ValidationError('el archivo debe ser una imagen')

    @staticmethod
    def validate_video(file):
        if not file:
            raise ValidationError('No se ha proporcionado ningún archivo')
        if file.content_type != 'video/mp4':
            raise ValidationError('El archivo debe ser de formato MP4')