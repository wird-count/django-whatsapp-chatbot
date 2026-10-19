from django.db import models

# Create your models here.

class Conversation(models.Model):
    phone_number = models.CharField(max_length=20,unique=True,db_index=True)
    summary = models.TextField(blank=True,default='')
    last_message_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.phone_number

class ProcessedMessage(models.Model):
    'evite de traite deux fois le meme message '
    wa_id = models.CharField(max_length=100,unique=True)
    created_at = models.DateField(auto_now_add=True)