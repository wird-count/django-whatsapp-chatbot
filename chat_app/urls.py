from django.urls import path,include
from . import views,views2

from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('webhook/',views.webhook,name='webhook'),#sauf meta qui lui fait appel a traveers le webhookconfiguration 
    path('auto/',views.trigger_avis_a_nos_client , name = 'trigger_avis_a_nos_client'),
    path('',views2.authentication,name='authentification'),
    path('ia_management',views2.ia_management,name='ia_management'),
    path('dz-rent-car',views2.dz_rent_car,name='dz-rent-car'),
    path('ajouter-vehicul-dz',views2.vehicul_exist,name='ajouter_vehicul-dz'),
    path('vehicules-suggestions/',views2.rechercher_vehicules,name='vehicules-suggestions'),
    path('QR-code',views.QR_code,name='QR_code'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )





