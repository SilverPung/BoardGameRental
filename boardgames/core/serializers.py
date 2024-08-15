from rest_framework import serializers
from .models import Game



class GameSerializer(serializers.ModelSerializer):

    class Meta:
        model = Game
        fields = 'title','barcode','description','event','min_players','max_players','min_playtime','max_playtime','categories','mechanics'


