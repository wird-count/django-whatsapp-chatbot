from django.urls import path,include

from . import views



urlpatterns = [
    path('',views.lancee_une_requette),
]


# prenant lexemple de meta 
# project = meta 
# app1 = facebook
# app2 = instagram 
# app3 = whatsapp
# les trois app discutes on le sais tres bien (les pub de vetement que on sais interesser dans insta peut apparaite sur notre facebook) donc cest grace a la logic du 'REST API'