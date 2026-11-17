from django.contrib import admin

# Register your models here.
from .models import Vehicule

@admin.register(Vehicule)
class VehiculeAdmin(admin.ModelAdmin):
    list_display = ('marque', 'modele', 'annee', 'disponible', 'nouveaute')