from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Event,Game  # Replace MyModel with the name of your model

admin.site.register(Event)
admin.site.register(Game)