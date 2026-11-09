from django.shortcuts import render

# Create your views here.
import requests
from requests import auth
endpoint  = 'http://localhost:8000/api?abc=123'
import json
i = 0
def lancee_une_requette(request):
    global i
    if i>0 :
        print(f'111 - {request.GET.get('key')}')
        print(f'222 - {request.GET.get('abc')}')
    i+=1
    import requests
 
    endpoint = 'http://localhost:8000/api/?abc=123'
    return requests.get(endpoint)

    session = requests.Session()

    # 1. Demander le cookie CSRF
    csrf_response = session.get(
        'http://localhost:8000/api/csrf/'
    )

    print(csrf_response.status_code)
    print(csrf_response.json())

    # 2. Récupérer le token
    csrf_token = session.cookies.get('csrftoken')

    print("CSRF Token :", csrf_token)


    get_response = session.post(endpoint,
                                headers={'X-CSRFToken': csrf_token}
                                )#HTTP requests donc quand on envoie une request manuelle evec python rest api (contrairement a automatic avec postman) ici la request elle a des reponse donc que on devrais exploitez dailleur car cest tout a fait le principe des cette sychronization backend-backend 

   
    
    print(get_response.json().get('abc'))

    # print(get_response.get('abc'))
    print(get_response)
    print(type(json.loads(get_response.text)))
    print(get_response.status_code)
    print(get_response.url)
    print('_______')
    print(get_response.headers)
    print('_______')

# remarc :
# http request --> HTML
# rest api http request --> json



