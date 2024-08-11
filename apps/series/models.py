from django.db import models

class Genre(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=25)

    def __str__(self) -> str:
        return self.name

class SerieStatus(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=25)

    def __str__(self) -> str:
        return self.name

class Series(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, null= None)
    description = models.TextField(null=None)
    release_date = models.DateField(null=None)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE) #El principal?
    image_url = models.URLField(blank=True, null=None)
    rating = models.IntegerField()
    status = models.ForeignKey(SerieStatus, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.title

class Episodes(models.Model):
    id = models.AutoField(primary_key=True)
    series_id = models.ForeignKey(Series, on_delete=models.CASCADE, null=None)
    title = models.CharField(max_length=255, null=None)
    episode_number = models.IntegerField(null=None)
    release_date = models.DateField()
    video_url = models.TextField(null=None)
    thumbnail_url = models.TextField(null=None) #miniatura