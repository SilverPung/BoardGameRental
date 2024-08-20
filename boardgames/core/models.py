from typing import Iterable
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
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
    
class KnownDistributor(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE,default=None, blank=True,null=True)
    distributor = models.CharField(max_length=100)
    
    def __str__(self):
        return self.distributor

class Game(models.Model):

    barcode = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=100)
    distributor = models.CharField(max_length=100)
    event = models.ForeignKey(Event, on_delete=models.CASCADE,default=None, blank=True,null=True)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    accessible = models.IntegerField(null=True, blank=True)
    quantity = models.IntegerField()
    list_of_renters = models.ManyToManyField('Renter', related_name='rented_games',default=None, blank=True)
    avg_rating = models.FloatField(default=0)
    rating_count = models.IntegerField(default=0)
    top= models.BooleanField(default=False)
    comments= models.TextField(null=True, blank=True)

    min_players = models.IntegerField(null=True, blank=True)
    max_players = models.IntegerField(null=True, blank=True)
    min_playtime = models.IntegerField(null=True, blank=True)
    max_playtime = models.IntegerField(null=True, blank=True)
    categories = models.TextField(null=True, blank=True)
    mechanics = models.TextField(null=True, blank=True)
    complexity = models.FloatField(null=True, blank=True)


    def save(self,*args, **kwargs):
        self.distributor=self.distributor.capitalize()
        self.title=self.title.capitalize()
        
        if not self.pk:  
            self.accessible = self.quantity  
        super(Game, self).save(*args, **kwargs)  
        if self.distributor and not KnownDistributor.objects.filter(event=self.event, distributor=self.distributor.capitalize()).exists():
            known_distributor = KnownDistributor(event=self.event, distributor=self.distributor)
            known_distributor.save()

    def add_renter(self, barcode):
        if renter := Renter.objects.filter(barcode=barcode).first():
            if not self.list_of_renters.filter(id=renter.id).exists():
                self.list_of_renters.add(renter)
                self.accessible -= 1
                renter.how_many_games += 1
                renter.save()
                self.save()
                
        else:
            renter = Renter(barcode=barcode)
            renter.save()
            renter.event = self.event
            renter.save()
            renter.how_many_games += 1
            renter.save()
            self.list_of_renters.add(renter)
            self.accessible -= 1
            self.save()
    
    def add_rating(self, rating):
        self.avg_rating = (self.avg_rating * self.rating_count + float(rating)) / (self.rating_count + 1)
        self.rating_count += 1
        self.save()        
    
    def __str__(self):
        return self.title  
    
class Renter(models.Model):
    barcode = models.CharField(max_length=20)
    event = models.ForeignKey(Event, on_delete=models.CASCADE,default=None, blank=True,null=True)
    list_of_games = models.ManyToManyField(Game, related_name='rented_games',default=None, blank=True)
    how_many_games = models.IntegerField(default=0)

    def __str__(self):
        return self.barcode
    
