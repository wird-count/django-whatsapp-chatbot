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
# on recoie  une reponse quellqueonque dapres le prompt inserer et le user_text
def call_gemini(prompt , user_text):
    url = f'https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent'
    try:
        r = requests.post(
            url,
            headers={'x-goog-api-key': GEMINI_API_KEY},
            json={
                'systemInstruction': {'parts': [{'text': prompt}]},
                'contents': [{'role': 'user', 'parts': [{'text': user_text}]}],
            },
            timeout=30,
        )
        if r.ok:
            print('DETAIL IA :', r.status_code, r.text)
            return r.json()['candidates'][0]['content']['parts'][0]['text']
        return None
    except Exception as e:
        print('ERREUR IA :', repr(e))
        return None


# on recoie la reponse pour la disscussion actuel
def ask_ia(user_text,previous_summary=''):
    system = SYSTEM_PROMPT
    if len(previous_summary) : # ca dire on verifie si la varaible vide --> false , remplise -->True
        system += (
            "\n\nRésumé des échanges précédents avec ce client "
            "(utilise-le pour assurer la continuité, sans le réciter) :\n"
            + previous_summary
        )
    response =  call_gemini(system,user_text)
    return response or 'desole , yas un souci veullez reesayer uterieurement'


# on recoie le prompt que on vas enregistrer dans le phone number equivalent (combinaision encien prommot + nouvel disscoussion)
def update_sammary(old_summary,user_text,ai_reply):
    prompt = (
        f"Résumé actuel :\n{old_summary or '(aucun)'}\n\n"
        f"Nouvel échange :\nClient : {user_text}\nAssistant : {ai_reply}\n\n"
        "Mets à jour le résumé en 150 mots maximum : infos sur le client, "
        "véhicule(s) recherché(s), budget, décisions prises, points en suspens. "
        "Retourne uniquement le résumé, sans introduction."        
    )
    new_summary = call_gemini('Tu produis des résumés concis et factuels.',prompt)
    return new_summary or old_summary # en cas ou lia ne defaillante on garde lancienne prompt 

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
                    phone = m['from']
                    text = m['text']['body']
                    print('RECU',phone,text)

                    from .models import Conversation , ProcessedMessage
                    _,created = ProcessedMessage.objects.get_or_create(wa_id=m['id'])  # anti-doublon
                    if not created :
                        continue
                    conv ,_   = Conversation.objects.get_or_create(phone_number=phone)   # 1. retrouver (ou créer) la conversation de ce numéro

                     # 2. l'IA reçoit l'ancien résumé
                    ai_reply = ask_ia(text,conv.summary)
                    send_text(phone,ai_reply)

                    # 3. on réinjecte le nouveau résumé dans la DB
                    conv.summary = update_sammary(conv.summary,text,ai_reply)
                    conv.save()



        except (KeyError,IndexError) as e :
            print(f'erreur lecture message : {repr(e)}')

        return JsonResponse({'status':'ok'})
    
    return HttpResponse(status=405) # not POST not GET ==> attentive de connnection dun robot ==> erreur emidiate





    