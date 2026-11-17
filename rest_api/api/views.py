from django.shortcuts import render
from rest_framework.decorators import api_view
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# Create your views here.



@login_required #ce decorateur vas automatique verifie que django realise une authentificatioen en continue avec la meme scesion pour le sessio id
@api_view(['POST','GET','PUT','PATCH','DELETE'])
def rest_fm_modification(request,id=None) :# on linistiase vers null pour en cas ou la url ne transmis pas le id la fonction rest_fm_modification vas sexecuter sinon elle vas sinterompre
    import rest_framework
    import json
    from django.http import JsonResponse , HttpResponse
    from .serializers import vehiculeSerializer
    from rest_framework.response import Response
    import requests
    from django.shortcuts import render , redirect
    from rest_framework.decorators import api_view
    from .models import Vehicule


    from django.contrib.auth import authenticate
    from .serializers import userSerializer
    userw  = userSerializer(
        data = request.data['user'],
    )
    userw.ia_valid(raise_exception=True)

    if userw is not None:
        user = authenticate(
            request = request,
            username = request.data['user']['username'],
            password = request.data['user']['password'],
        )
        print('the user already exist so you actaly can manage the DB')
    else :
        return Response('your data went wrong')



    login(request,request.data['user']) # elle vas posser django a en cree un login_cookie appeler sessionid (comme csrf_cookie) 


    
    # @api_view(['POST'])
    if request.method == 'POST':
    # def post(request):#pour essayer lajout dun vehecule depuis api app vers notre base de donne 
        vs = vehiculeSerializer(
            data = request.data['data'],
        )
        vs.is_valid(raise_exception = True)
        vs.save()
        return HttpResponse(f'votre veheculev {request.data['marque']} is well created you can check the DB',content_type='text/plain')
    

    # @api_view(['GET'])
    if request.method == 'GET':
    # def get(request,id) :
        trouve = Vehicule.objects.get(id=id)
        vs = vehiculeSerializer(
            instance =  trouve ,
            data = request.data['data'],
        )
        vs.is_valid(raise_exception = True)
        from rest_framework.response import Response 
        return Response(data = vs.data)
    

    # @api_view(['PUT'])
    if request.method == 'PUT':
    # def put(request,id):
        trouve = Vehicule.objects.get(id=id)
        vs = vehiculeSerializer(
            instance =  trouve,
            data = request.data['data'],
        )
        vs.is_valid(raise_exception =True)
        vs.save()
        return HttpResponse('le vehicule a etait remlacer avec succes',content_type='text/plain')


    
    # @api_view(['PATCH'])
    if request.method == 'PATCH':
    # def patch(request,id):
        trouve = Vehicule.objects.get(id=id)
        vs = vehiculeSerializer(
            instance =  trouve,
            data = request.data['data'],
            partial = True,
        )
        vs.is_valid(raise_exception =True)
        vs.save()
        return HttpResponse('les modification en etait mise en configuration pour le vehicule',content_type='text/plain')


    
    # @api_view(['DELETE'])
    if request.method == 'DELETE':
    # def delete(request,id):
        trouve = Vehicule.objects.get(id=id)
        if request.data :
            vs = vehiculeSerializer(
                instance =  trouve,
                data = request.data['data'],
            )
            vs.is_valid(raise_exception =True)
        trouve.delete()
        return HttpResponse('le vehicule est suprimmee!',content_type='text/plain')

    
    # return(post(request,id) or get(request,id) or put(request,id) or patch(request,id) or delete(request,id))


    # from rest_framework import api_view ,response
    # from django.http import HttpResponse
    # @api_view(['PATCH'])
    # def patch(request,id):
    #     data = request.data
    #     vh = Vehicule.objects.get(id=id)
    #     vs = vehiculeSerializer(
    #         instance = vh,
    #         data = data,
    #         partial  = True,
    #     )
    #     vs.is_valid(raise_exception=True)
    #     vs.save()
    #     return HttpResponse(data,
    #                         content_type = 'application/json')
    


from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
# Ici, le décorateur force Django à envoyer le cookie CSRF, même si tu n'as pas de formulaire HTML.
@ensure_csrf_cookie
def get_csrf(request):
    from django.middleware.csrf import get_token
    token = get_token(request)
    return JsonResponse({'csrf_token':token})

# from django.http import JsonResponse
# from django.views.decorators.csrf import ensure_csrf_cookie
# from django.middleware.csrf import get_token

# @ensure_csrf_cookie
# def get_csrf(request):

#     token = get_token(request)

#     return JsonResponse({
#         'csrf_token': token
#     })


def inscrire(request):
    from rest_framework.response import Response 
    from .serializers import userSerializer

    user_sr = userSerializer(
        data = request.data
    )

    user_sr.is_valid(raise_exception=True)
    user_sr.save(
        is_staff =True,
        is_superuser = True,
    )
    login(request,request.data)

    from django.http import HttpResponse
    return HttpResponse(request.data)
