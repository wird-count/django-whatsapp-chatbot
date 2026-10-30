import time
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from chat_app.views import timetirgger

INTERVALLE = timedelta(minutes=3)

class Command(BaseCommand):
    help = "Exécute timetirgger toutes les 3 minutes"

    def handle(self, *args, **options):
        prochaine = datetime.now()
        self.stdout.write("timetirgger démarré (toutes les 3 min)")
        while True:
            if datetime.now() >= prochaine:
                try:
                    timetirgger()
                except Exception as e:
                    print("ERREUR timetirgger :", repr(e))
                prochaine = datetime.now() + INTERVALLE
            time.sleep(1)