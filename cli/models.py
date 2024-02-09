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
    average_rating = models.FloatField(default=0)

    def __str__(self):
        return self.primaryTitle

class Name(models.Model):
    nameID = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    namePoster = models.URLField(blank=True, null=True)
    birthYear = models.IntegerField(null=True, blank=True)
    deathYear = models.IntegerField(null=True, blank=True)
    profession = models.CharField(max_length=255, blank=True, null=True)
    # Assuming nameTitles is a Many-to-Many relationship to the Movie model
    nameTitles = models.ManyToManyField(Movie, through='Participation')
    # titleID and category will be part of the Participation model

    def __str__(self):
        return self.name

class Participation(models.Model):
    name = models.ForeignKey(Name, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    category = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name.name} - {self.movie.primaryTitle} ({self.category})"