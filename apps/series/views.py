from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Genre, Series, Episodes
from .serializers import GenderSerializer, SeriesSerializer, EpisodesSerializer

class GenreView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Genre.objects.all()
    serializer_class = GenderSerializer

class SeriesView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Series.objects.all()
    serializer_class = SeriesSerializer

class EpisodesView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    queryset = Episodes.objects.all()
    serializer_class = EpisodesSerializer