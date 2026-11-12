from django.shortcuts import render
from django.http import JsonResponse
import requests
import json
# Create your views here.
from chat_app.admin import Vehicule
def func(request):
    print(f'request.body : {request.body}\n')
    print(f'request.params : {request.GET.get('para1')}\n')#1. request.GET : récupérer les paramètres de l'URL Les données sont transmises directement dans l'URL, après le symbole ?.
    # print(f'requesrt.params.POST {request.POST}')
    data = {}
    data['vehicules disponible']= list(Vehicule.objects.filter(disponible=True).values('marque','modele'))
    data['headers'] = dict(request.headers)
    # data = json.dumps(data, ensure_ascii=False)
    data['abc']=request.GET.get('abc')# car on a passe abc comme parametre
    # return JsonResponse(data,safe=False)

    endpoint_chatapp2 = 'http://localhost:8001/chat_app2/?abc=123'
    return requests.get(url = endpoint_chatapp2,params={'key':'value / im the parameter sent withing the request from api ---> chatapp2'})






# remarque : a request transmit tout sorte de donne soit parameters ou GET(envoie) ou POST(reception)

from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie

@ensure_csrf_cookie
def get_csrf(request):
    return JsonResponse({
        'message': 'CSRF cookie created'
    })




def modify_in_chatapp_restapi(request):
    endpoint = 'http://localhost:8001/chat_app/'
    car_id = input('veullez inserer le id du vehicule dont vous en voulez completer des modification !')
    url = endpoint + '{car_id}/'
    # marque = request.POST.get('marque')
    # anne = request.POST.get('anne')
    data = {'annee':2026,
            'marque' : 'GAC',
            }
    return(requests.put(url = endpoint,data = data))




def let_manipulate_our_api_from_here(request):
    url_post = 'http://localhost:8000/rest_fm_modification'
    import requests
    rq = requests

