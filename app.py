from flask import Flask, render_template, request
import os
import requests

# === Configuration Telegram ===
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "7473580823:AAHlqSw9noRCHDP4S2x2akrz3iJubVH74iI")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "@Sisu1013")

# === Initialisation de l'application Flask ===
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/commander', methods=['POST'])
def commander():
    # Récupère les données du formulaire
    nom = request.form.get('nom')
    telephone = request.form.get('telephone')
    quantite = request.form.get('quantite') or "1"
    plats = request.form.getlist('plats[]')
    boisson = request.form.get('boisson') or "Aucune"

    print("=== NOUVELLE COMMANDE ===")
    print(f"Nom : {nom}")
    print(f"Téléphone : {telephone}")
    print(f"Plats : {', '.join(plats)} x{quantite}")
    print(f"Boisson : {boisson}")
    print("===========================")

    # Prépare le message Telegram
    message = "*Nouvelle commande reçue !*\n\n"
    message += f"Client : {nom}\n"
    message += f"Téléphone : {telephone}\n"
    message += f"Plats : {', '.join(plats)} x{quantite}\n"
    message += f"Boisson : {boisson}"

    # Envoie via Telegram
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage" 
        data = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "Markdown"
        }
        response = requests.post(url, data=data)
        print("✅ Message envoyé sur Telegram", response.json())
    except Exception as e:
        print("❌ Échec d'envoi Telegram", str(e))

    # Réponse au client
    return """
        <h2>Merci pour votre commande !</h2>
        <p>Nous vous contacterons bientôt.</p>
        <a href="/">Retour au menu</a>
    """