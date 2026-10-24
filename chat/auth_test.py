from google_auth_oauthlib.flow import InstalledAppFlow
import pickle
import os

# Les permissions nécessaires pour Google Sheets et Drive
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

def main():
    # Cette méthode va lancer un serveur local et ouvrir votre navigateur pour vous connecter à votre compte Google
    flow = InstalledAppFlow.from_client_secrets_file(
        'client_secret.json', SCOPES) # (Voir note ci-dessous si vous n'avez pas ce fichier)
    creds = flow.run_local_server(port=0)
    
    # Sauvegarde des credentials dans un fichier token.pickle
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)
    print("Authentification réussie ! Token sauvegardé.")

if __name__ == '__main__':
    main()