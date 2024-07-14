from django.db import models
from django.utils import timezone
# Create your models here.


class Event(models.Model):
    
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    date = models.DateTimeField()
    def save(self, *args, **kwargs):
        if not self.id:  # If the instance is new, set the date to now
            self.date = timezone.now()
        super(Event, self).save(*args, **kwargs)

    def __str__(self):
        return self.title
    

class Game(models.Model):

    barcode = models.CharField(max_length=20)
    title = models.CharField(max_length=100)
    distributor = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='game_images', null=True, blank=True)
    quantity = models.IntegerField()
    bgg_url = models.URLField(null=True, blank=True)
    


    def __str__(self):
        return self.title