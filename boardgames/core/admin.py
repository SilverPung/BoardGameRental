from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Event,Game,Renter

admin.site.register(Event)
admin.site.register(Game)
admin.site.register(Renter)