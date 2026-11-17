from django.shortcuts import render
import json
# Create your views here.

def inscription():
    
    from django.contrib.auth.models import User
    from django.contrib.auth import authenticate
    from django.contrib.auth.hashers import make_password
    from django.shortcuts import render,redirect
    import requests
    from django.middleware.csrf import get_token
    from rest_framework import serializers
    import json
    user1 = {
        'username' : input('insert your username = '),
        'password' : input('insert your password = '),
        'email' : input('insert you email = '),
    }
    session ,csrf_token =  lunch_csrf_request(url = 'http://localhost:8001/api/get_csrf/')
    r = session.post(url = 'http://localhost:8001/api/inscrire/' , json=user1)
    if r.status_code == 200:
        sc = session.post(url='http://localhost:8001/requester',json=user1,headers = {'X-CSRFToken':csrf_token}) 
        












def let_manipulate_our_api_from_here(request):
    from rest_framework.response import Response
    from django.contrib.auth import authenticate,login,logout
    from django.contrib.auth.models import User
    # from rest_framework.response import Response
    # from rest_framework.decorators import api_view
    # from rest_framework import serializers


    url_post = 'http://localhost:8001/api/rest_fm_modification/'
    import requests
    
    
    data = {
        'marque' : 'renault',
        'modele' : 'symbol',
        'annee': 2025,
        'disponible' : True , #cest la ou le json.dumps doit intervenir
    }
    data_user = {
        'data':data,
        'user':request.data
    } 
    
    session , csrf_token = lunch_csrf_request(url='http://localhost:8001/api/get_csrf/')
    rq = session.post(url = url_post,json=data_user,headers={'X_CSRFToken':csrf_token})
    print('STATUT :', rq.status_code)
    print('REPONSE :', rq.text)
    rq = requests.get(url=(url_post+'3/'))#je vais rien modifier dans la base de donne donc pas la peine dune CSRF verification
    print('STATUT :', rq.status_code)
    print('REPONSE :', rq)
    rq = session.put(url=(url_post+'5/'),data = data_user,headers={'X_CSRFToken':csrf_token})
    print('STATUT :', rq.status_code)
    print('REPONSE :', rq.text)
    rq = session.patch(url = (url_post+'6/'),data = data_user,headers={'X_CSRFToken':csrf_token})
    print('STATUT :', rq.status_code)
    print('REPONSE :', rq.text)
    rq = session.delete(url = url_post + '2/',data = data_user,headers={'X_CSRFToken':csrf_token})
    print('STATUT :', rq.status_code)
    print('REPONSE :', rq.text)
    rq = session.get(url =  url_post + '7/',json=data_user,headers={'X_CSRFToken':csrf_token})
    # print('STATUT :', rq.status_code)
    # print('REPONSE :', rq.json()['marque'])
    print('STATUT :', rq.status_code)
    print('CONTENU :', repr(rq.text))
    print('TYPE :', rq.headers.get('Content-Type'))
    session.cookies.clear()
    session.close()

    from django.http import HttpResponse
    return HttpResponse('post,get,put,patch,delete',
                        content_type='text/plain')















def lunch_csrf_request(url='http://localhost:8001/api/get_csrf/'):
    import requests
    session = requests.Session()
    response = session.get(url=url)


    return session , response.json()['csrf_token'] # session qui vas comparer entre le token generer par le backend et celui envoyer par le client
    




# from django.views.decorators.csrf import ensure_csrf_cookie

# @ensure_csrf_cookie
# def get_csrf(request):
#     from django.http import JsonResponse
#     import requests
#     csrfed_request  requests.session()
#     csrfed_request = csrfed_request.get(url='http://localhost:8001/api/rest_fm_modification/')

#     return JsonResponse(
#         ''
#     )



