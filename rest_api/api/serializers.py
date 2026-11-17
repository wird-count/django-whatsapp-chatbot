from rest_framework import serializers
from .models import Vehicule
class vehiculeSerializer(serializers.ModelSerializer):  
    class Meta :
        model = Vehicule
        fields = '__all__'


from django.contrib.auth.models import User
class userSerializer(serializers.ModelSerializer):
    class meta :
        model  = User
        field = '__all__'

