from django.db import models

# Create your models here.

class Conversation(models.Model):
    phone_number = models.CharField(max_length=20, unique=True, db_index=True)
    summary = models.TextField(blank=True, default='')
    ia_response = models.BooleanField(default=True)    # <- nouveau
    last_message_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.phone_number

class ProcessedMessage(models.Model):
    'evite de traite deux fois le meme message '
    wa_id = models.CharField(max_length=100,unique=True)
    created_at = models.DateField(auto_now_add=True)




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