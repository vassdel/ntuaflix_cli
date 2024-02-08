from django.db import models

class Cli(models.Model):
  username = models.CharField(max_length=255)
  password = models.CharField(max_length=255)

class Movie(models.Model):
    tconst = models.CharField(max_length=255)
    titleType = models.CharField(max_length=255)
    primaryTitle = models.CharField(max_length=255)
    originalTitle = models.CharField(max_length=255)
    isAdult = models.BooleanField()
    startYear = models.IntegerField()
    endYear = models.IntegerField(null=True, blank=True)
    runtimeMinutes = models.IntegerField(null=True, blank=True)
    genres = models.CharField(max_length=255, null=True, blank=True)
    img_url_asset = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.primaryTitle
