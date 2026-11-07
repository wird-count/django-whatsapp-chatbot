from django.shortcuts import render
from django.http import JsonResponse
import json
# Create your views here.
from chat_app.admin import Vehicule
def func(request):
    print(f'request.body : {request.body}\n')
    return JsonResponse(data={'vehicules disponible pour lalocation ':list(Vehicule.objects.filter(disponible=True).values('marque','modele'))},)



