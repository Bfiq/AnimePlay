from rest_framework import serializers
from .models import Genre, Series, Episodes

class GenderSerializer(serializers.Serializer):
    class Meta:
        model = Genre
        fields = '__all__'

class SeriesSerializer(serializers.Serializer):
    class Meta:
        model = Series
        fields = '__all__'

class EpisodesSerializer(serializers.Serializer):
    class Meta:
        model = Episodes
        fields = '__all__'