from typing import Iterable
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.


class Event(models.Model):
    
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    date = models.DateTimeField()
    allowed_users = models.ManyToManyField(User, related_name='allowed_access',default=None)

    def save(self, *args, **kwargs):
        if not self.id:  # If the instance is new, set the date to now
            self.date = timezone.now()
        super(Event, self).save(*args, **kwargs)

    def add_default_users(self):
        self.allowed_users.add(User.objects.get(id=1))
        self.allowed_users.add(User.objects.get(id=2))
        self.save()

    def add_logged_in_user(self, user):
        if not self.allowed_users.filter(id=user.id).exists():
            self.allowed_users.add(user)
            self.save()

    def __str__(self):
        return self.title
    

class Game(models.Model):

    barcode = models.CharField(max_length=20)
    title = models.CharField(max_length=100)
    distributor = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='game_images', null=True, blank=True)
    accessible = models.IntegerField(null=True, blank=True)
    quantity = models.IntegerField()
    bgg_url = models.URLField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.pk:  # Check if the object is new
            self.accessible = self.quantity  # Set accessible to quantity before saving
        super(Game, self).save(*args, **kwargs)  # Call the "real" save() method.

    def __str__(self):
        return self.title