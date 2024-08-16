from django.urls import path
from .views import GenreView, SeriesView, EpisodesView, CommentsView

urlpatterns = [
    path('genre', GenreView.as_view(), name='genre'),
    path('series', SeriesView.as_view(), name='series'),
    path('episodes', EpisodesView.as_view(), name='episodes'),
    path('comments', CommentsView.as_view(), name='comments'),
]