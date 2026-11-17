from django.urls import path,include
from .views import rest_fm_modification,get_csrf , inscrire
urlpatterns = [
    path('rest_fm_modification/',rest_fm_modification,name='rest_fm_modification'),
    path('rest_fm_modification/<int:id>/',rest_fm_modification,name='rest_fm_modification'),
    path('get_csrf/',get_csrf,name='get_csrf'),
    path('inscrire/',inscrire,name = 'inscire'),
]




