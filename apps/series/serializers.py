from rest_framework import serializers
from .models import Genre, Series, Episodes
from apps.utils.validation_image import ValidationImage

class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class SeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Series
        fields = '__all__'
        extra_kwargs = {'image_url':{'read_only': True}}

    def validate(self, data):
      
        image = self.context['request'].FILES.get('image')
        print('AQUI?')
        if image:
            print('ENTRE?')
            ValidationImage.validate(image)
        return data

class EpisodesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episodes
        fields = '__all__'