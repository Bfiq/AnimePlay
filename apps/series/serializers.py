from rest_framework import serializers
from .models import Genre, Series, Episodes

class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class SeriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Series
        fields = '__all__'
        extra_kwargs = {'image_url':{'read_only': True}}

class EpisodesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episodes
        fields = '__all__'