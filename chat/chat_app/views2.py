from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render , redirect
from django.contrib.auth import authenticate,login,logout
from .admin import Conversation
def authentication(request):
    if request.method == 'GET':
       return render(request,'html/authentication.html')
    else :
        user = authenticate(
            request ,
            username = request.POST.get('username').strip(),
            password = request.POST.get('password',''),
        )
        if user is not None :
            login(request,user)
            return redirect('ia_management')
        else : 
            messages.error(request,'veuillez resesir vos cordonnee , merci !')
            return(request,'html/authentication.html')

@staff_member_required
def ia_management(request):
    if request.method == 'POST':
        phone = request.POST.get('phone_number', '').strip().replace(' ', '').lstrip('+')
        client = Conversation.objects.filter(phone_number=phone).first()
        if client is None:
            messages.error(request, "Client introuvable.")
        else:
            client.ia_response = not client.ia_response    # bascule
            client.save(update_fields=['ia_response'])
            etat = "réactivée" if client.ia_response else "désactivée"
            messages.success(request, f"IA {etat} pour {client.phone_number}.")
        return redirect('ia_management')
    return render(request, 'html/ia_management.html')
        




                

def dz_rent_car(request):
    from .models import Vehicule
    vh = Vehicule.objects.filter(location=True).order_by('-created_at')
    if vh == None :
        return render(request,'html/dz_rent_car.html')
    return render(request,'html/dz_rent_car.html',{'vehicules':vh})



    



from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Vehicule


def ajouter_vehecul(request):
    if request.method == 'POST':
        marque = request.POST.get('marque', '').strip()
        modele = request.POST.get('modele', '').strip()
        annee = request.POST.get('annee') or None
        prix = request.POST.get('prix') or None

        # Photo envoyée par le formulaire
        photo = request.FILES.get('photo')

        # Cases à cocher
        disponible = request.POST.get('disponible') == 'on'
        nouveaute = request.POST.get('nouveaute') == 'on'
        location = request.POST.get('location') == 'on'

        if not marque or not modele:
            messages.error(
                request,
                "Veuillez renseigner la marque et le modèle."
            )
            return render(request, 'html/ajouter_vehicule_dz.html')

        try:
            Vehicule.objects.create(
                marque=marque,
                modele=modele,
                annee=annee,
                prix=prix,
                disponible=disponible,
                nouveaute=nouveaute,
                location=location,
                photo=reduire_image(photo)
            )

            messages.success(
                request,
                "Le véhicule et sa photo ont été enregistrés."
            )
            return redirect('dz-rent-car')

        except (ValueError, TypeError):
            messages.error(
                request,
                "L'année ou le prix saisi est invalide."
            )

    return render(request, 'html/ajouter_vehicule_dz.html')


vehicul_index = -1
def reduire_image(fichier , max_px=1200, qualite=82):
    global vehicul_index
    vehicul_index +=1
    from io import BytesIO
    from django.core.files.base import ContentFile
    from PIL import Image,ImageOps

    img = Image.open(fichier)
    img = ImageOps.exif_transpose(img)   # respecte l'orientation des photos de téléphone
    img = img.convert('RGB')             # transparence PNG/WebP -> JPEG
    img.thumbnail((max_px, max_px))      # garde les proportions, ne grossit jamais
    sortie = BytesIO()
    img.save(sortie, 'JPEG', quality=qualite, optimize=True)
    return ContentFile(sortie.getvalue(), name=f'photo{vehicul_index}.jpg')
