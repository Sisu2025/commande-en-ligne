from flask import Flask, render_template, request
import requests

app = Flask(__name__, static_folder='static', template_folder='templates')

# === Paramètres Telegram ===
TELEGRAM_BOT_TOKEN = "7403862599:AAERC-FuhFQJyJERnJ8Zf-pE_FogHGVcc00"
TELEGRAM_CHAT_ID = "@saveurdebabi_bot"  # ou un ID de groupe (ex: -1001234567890)

# === URL de l'API Telegram ===
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage" 
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, data=data)
        print("✅ Message Telegram envoyé :", response.json())
    except Exception as e:
        print("❌ Échec d'envoi Telegram", str(e))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/commander', methods=['POST'])
def commander():
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

    # Création du message Telegram
    message = "*Nouvelle commande reçue !*\n\n"
    message += f"Client : {nom}\n"
    message += f"Téléphone : {telephone}\n"
    message += f"Plats : {', '.join(plats)} x{quantite}\n"
    message += f"Boisson : {boisson}"

    # Envoi via Telegram
    send_telegram_message(message)

    return """
        <h2>Merci pour votre commande !</h2>
        <p>Nous vous contacterons bientôt.</p>
        <a href="/">Retour au menu</a>
    """