from django.shortcuts import render , redirect
# from django.contrib import messages
# from django.apps.config import User
# from django.forms import Form

# Create your views here.

import json , os
from django.http import HttpResponse , JsonResponse , HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
import requests



VERIFY_TOKEN = os.getenv('VERIFY_TOKEN','test123') #Si vous ouvrez un autre terminal, elle est absente et Django utilise la valeur par défaut test123.
# VERIFY_TOKEN = 'test123'
WHATSAPP_TOKEN = os.getenv('WHATSAPP_TOKEN')
PHONE_NUMBER_ID = os.getenv('PHONE_NUMBER_ID')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
GRAPH_URL = 'https://graph.facebook.com/v21.0'

GEMINI_MODEL = os.getenv('GEMINI_MODEL','gemini-2.5-flash')
# GEMINI_MODEL='gemini-2.5-flash'
SYSTEM_PROMPT = (
    "Tu es l'assistant WhatsApp de vente de vehicul. "
    "Réponds en français, de façon courte et polie. "
    "Si tu ne connais pas la réponse, dis-le au lieu d'inventer."
)

def ask_ia(user_text):
    url = f'https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent'
    try:
        r = requests.post(
            url,
            headers={'x-goog-api-key': GEMINI_API_KEY},
            json={
                'systemInstruction': {'parts': [{'text': SYSTEM_PROMPT}]},
                'contents': [{'role': 'user', 'parts': [{'text': user_text}]}],
            },
            timeout=30,
        )
        if not r.ok:
            print('DETAIL IA :', r.status_code, r.text)
            return "Désolé, je rencontre un problème. Réessayez dans un instant."
        return r.json()['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        print('ERREUR IA :', repr(e))
        return "Désolé, je rencontre un problème. Réessayez dans un instant."


def send_text(to,body):
    r = requests.post(
        f'{GRAPH_URL}/{PHONE_NUMBER_ID}/messages',
        headers = {'authorization' : f'Bearer {WHATSAPP_TOKEN}'},
        json    = {'messaging_product':'whatsapp','to':to,'type':'text','text': {'body':body}},
        timeout = 10,
    )
    print('ENVOI : ' , r.status_code , r.text)


 

# decorators webhook(csrf_exempt(var))
@csrf_exempt # desactive la protection csrf de django car meta ne fournie aucune info sur la protection csrf depuis leur request
def webhook(request):
    if request.method == 'GET': 

        if (request.GET.get('hub.mode') == 'subscribe') and (request.GET.get('hub.verify_token') == VERIFY_TOKEN) :
            return HttpResponse(request.GET.get('hub.challenge'),content_type='text/plain') # cet le prince denvoie dun code sur ton numero de telephone pour verifie que cest reelment vous qui essay de se connecter a son compte
        # http://127.0.0.1:8000/webhook/?hub.mode=subscribe&hub.verify_token=test123&     hub.challenge=hello 
        else :
            return HttpResponseForbidden()
        
    if request.method == 'POST' :

        data = json.loads(request.body)
        try : 

            value = data['entry'][0]['changes'][0]['value']
            for m in value.get('messages',[]):
                if m.get('type') == 'text':
                    print('RECU',m['from'],m['text']['body'])
                    ai_reply = ask_ia(m['text']['body'])
                    send_text(m['from'],ai_reply)

        except (KeyError,IndexError) as e :
            print(f'erreur lecture message : {repr(e)}')

        return JsonResponse({'status':'ok'})
    
    return HttpResponse(status=405) # not POST not GET ==> attentive de connnection dun robot ==> erreur emidiate





    