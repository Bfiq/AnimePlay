from django.contrib import admin
from .models import Genre, Series, Episodes, SerieStatus

admin.site.register(Genre)
admin.site.register(Series)
admin.site.register(Episodes)
admin.site.register(SerieStatus)