from django.db import models

# Create your models here.
class Vehicule(models.Model):
    marque = models.CharField(max_length=50)
    modele = models.CharField(max_length=50)
    annee = models.PositiveSmallIntegerField(null=True, blank=True)
    prix = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    disponible = models.BooleanField(default=True)
    nouveaute = models.BooleanField("Nouveauté", default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    location = models.BooleanField(default=False)
    photo = models.ImageField(
        upload_to = 'vehicules/',
        null = True,
        blank = True,
    )

    def __str__(self):
        return f"{self.marque} {self.modele}"