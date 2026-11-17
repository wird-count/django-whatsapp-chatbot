from django.urls import path , include
from .views import let_manipulate_our_api_from_here,inscription
urlpatterns = [
    path('',let_manipulate_our_api_from_here,name='let_manipulate_our_api_from_here'),
    path('inscription/',inscription,name='inscription'),
]



