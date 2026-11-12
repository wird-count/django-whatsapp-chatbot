from rest_framework import serializers
from models import Vehicule
class vehiculeSerializer(serializers.ModelSerializer):  
    class Meta :
        model = Vehicule
        fields = '__all__'



