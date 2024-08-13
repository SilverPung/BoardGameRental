from rest_framework import serializers
from .models import Game,Event



class GameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Game
        fields = 'title','barcode','distributor','description','event','top'



