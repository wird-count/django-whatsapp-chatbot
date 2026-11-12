from django.urls import path , include
from . import views3

urlpatterns = [
    path('rest_fm_modification',views3.rest_fm_modification,name='rest_fm_modification'),  #dans le cas ou on avait une post method
    path('rest_fm_modification/<int:id>',views3.rest_fm_modification,name='rest_fm_modification'),
]