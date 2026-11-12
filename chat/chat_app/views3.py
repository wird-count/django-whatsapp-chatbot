# def rest_fm_modification(request):
#     import requests
#     from models import Vehicule
#     from django.http import JsonResponse , rsponse
#     import json
#     from serializers.serializer import Vehiculeserializer
#     if request.method == 'get':
#         vh = list(Vehicule.objects.filter(id=request.GET.get('id')))
#         return JsonResponse(vh)
#     elif request.method == 'post':
#         vh = Vehicule.objects.create(
#             marque = request.POST.get('marque'),
#         )
#         vh.save()
#     elif request.method == 'patch':

#         serializer = Vehiculeserializer(
#             instance = Vehicule.objects.get(marque=request.GET.get('marque'),anne = request.GET.get('annee')),
#             data = json(request.params()),
#             partial = True,
#         )
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return requests.get(url =request.url ,data=serializer())
#     elif request.method == 'patch':
#         import json
#         from django.http import JsonResponse , httpResponse
#         data = json.loads(request.data)
#         instance = Vehicule.objects.get(id = request.data('id'))
#         instance.delete()

#         data = json.dumps()
        
#         return httpResponse()
    

def rest_fm_modification(request,id=None) :# on linistiase vers null pour en cas ou la url ne transmis pas le id la fonction rest_fm_modification vas sexecuter sinon elle vas sinterompre
    import rest_framework
    import json
    from django.http import JsonResponse , HttpResponse
    from serializers import vehiculeSerializer
    from rest_framework import response
    import requests
    from django.shortcuts import render , redirect
    from rest_framework import api_view
    from models import Vehicule
    # @api_view(['POST'])
    if request.method == 'POST':
    # def post(request):#pour essayer lajout dun vehecule depuis api app vers notre base de donne 
        vs = vehiculeSerializer(
            instance = request.data,
        )
        vs.is_valid(raise_exception = True)
        vs.save()
        return HttpResponse(f'votre veheculev {request.json()['marque']} is well created you can check the DB')

    # @api_view(['GET'])
    if request.method == 'GET':
    # def get(request,id) :
        trouve = Vehicule.objects.get(id=id)
        vs = vehiculeSerializer(
            instance =  trouve ,
            data = request.data,
        )
        vs.is_valid(raise_exception = True)
        return JsonResponse(trouve)

    # @api_view(['PUT'])
    if request.method == 'PUT':
    # def put(request,id):
        trouve = Vehicule.objects.get(id=id)
        vs = vehiculeSerializer(
            instance =  trouve,
            data = request.data,
        )
        vs.is_valid(raise_exception =True)
        vs.save()
        return HttpResponse('le vehicule a etait remlacer avec succes')
    # @api_view(['PATCH'])
    if request.method == 'PATCH':
    # def patch(request,id):
        trouve = Vehicule.objects.get(id=id)
        vs = vehiculeSerializer(
            instance =  trouve,
            data = request.data,
        )
        vs.is_valid(raise_exception =True)
        vs.save()
        return HttpResponse('les modification en etait mise en configuration pour le vehicule')
    # @api_view(['DELETE'])
    if request.method == 'delete':
    # def delete(request,id):
        trouve = Vehicule.objects.get(id=id)
        if request.data :
            vs = vehiculeSerializer(
                instance =  trouve,
                data = request.data,
            )
            vs.is_valid(raise_exception =True)
        trouve.delete()
        return HttpResponse('le vehicule est suprimmee! ')
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
    
