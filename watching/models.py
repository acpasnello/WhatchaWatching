from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class User(AbstractUser):
    pass

class List(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mylists')
    # contributors = models.
    # private = models.BooleanField(default=False)

class ListItem(models.Model):
    # Define media type options
    media_types = [
    ('M', 'Movie'),
    ('S', 'Show'),
    ]

    list = models.ForeignKey(List, on_delete=models.CASCADE, related_name='listitems')
    itemID = models.IntegerField() # will be the ID, so you can look for a Media object or search TMDB
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=20, choices=media_types)
    poster = models.CharField(max_length=200, null=True)

    def __str__(self):
        return '%s on %s of %s' % (self.name, self.list.name, self.list.owner.username)

class Media(models.Model):
    # Define media type options
    MOVIE = 'M'
    SHOW = 'S'
    media_types = [
    (MOVIE, 'Movie'),
    (SHOW, 'Show'),
    ]

    id = models.IntegerField(primary_key=True)
    type = models.CharField(max_length=20, choices=media_types) #needs options: movie, tv
    poster = models.URLField()

class Rating(models.Model):
    # Define media type options
    MOVIE = 'M'
    SHOW = 'S'
    media_types = [
    (MOVIE, 'Movie'),
    (SHOW, 'Show'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='myRatings')
    subject = models.IntegerField()
    subjecttype = models.CharField(max_length=20, choices=media_types)
    name = models.CharField(max_length=200)
    rating = models.DecimalField(max_digits=3, decimal_places=1, validators=[MinValueValidator(0.0), MaxValueValidator(10)])
    review = models.TextField(blank=True, default='')
    # datetime = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            'id': self.pk,
            'user': self.user.username,
            'userID': self.user.pk,
            'subject': self.subject,
            'subjecttype': self.subjecttype,
            'name': self.name,
            'rating': self.rating,
            'review': self.review
        }