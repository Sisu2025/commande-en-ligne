from flask import Flask, render_template, request
import os
import requests

# === Configuration Telegram ===
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "7149326306:AAHKTAJYiHwr2VsRiRPyfkp4U2Ry-VY4Uyw")
TELEGRAM_CHAT_ID_1 = os.getenv("TELEGRAM_CHAT_ID_1", "5033835311")  # Premier compte
TELEGRAM_CHAT_ID_2 = os.getenv("TELEGRAM_CHAT_ID_2", "7591845004")    # Deuxième compte

# === Dictionnaire des frais de livraison (par ordre alphabétique) ===
frais_livraison = {
    "Abatta": 1500,
    "Abobo": 1500,	
    "Adjamé": 2000,
    "Angre": 1000,
    "Attécoubé": 2000,
    "Bingerville": 2000,
    "Cocody": 1500,
    "Deux plateaux": 1500,
    "plateau dokui": 1500,
    "Koumassi": 2500,
    "Marcory": 2500,
    "Plateau": 2000,
    "Riviera 2": 1500,
    "Riviera 3 4": 1500,
    "Riviera Palmeraie": 1500,
    "Riviera faya": 2000,
    "Treichville": 2500,
    "Yopougon": 2500
}

# === Dictionnaire des accompagnements avec leurs prix ===
accompagnements_prix = {
    "Riz": 1000,
    "Ignames grillés": 1000,
    "Claclo": 1000,
    "Attieké huile rouge": 1000,
    "Alloco": 1000
}

# === Création de l'application Flask ===
app = Flask(__name__, static_folder='static', template_folder='templates')


# === Fonction d'envoi Telegram ===
def send_telegram_message(message, chat_id):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"          
    data = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, data=data)
        if response.status_code == 200 and response.json().get("ok"):
            print(f"✅ Message envoyé à {chat_id}")
        else:
            error = response.json()
            print(f"❌ Échec d'envoi à {chat_id} - Erreur :", error.get("description", "Inconnue"))
    except Exception as e:
        print(f"🚨 Erreur lors de l'envoi à {chat_id} :", str(e))


# === Vérifie si le bot peut écrire à ce chat ID ===
def can_send_message(chat_id):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getChat"    
    data = {"chat_id": chat_id}
    try:
        response = requests.post(url, data=data)
        if response.status_code == 200 and response.json().get("ok"):
            return response.json()["result"].get("can_write_to_peer", False)
        else:
            print(f"🚫 Ne peut pas écrire à {chat_id} - Réponse API:", response.json())
    except Exception as e:
        print(f"🚨 Impossible de vérifier si on peut écrire à {chat_id} :", str(e))
    return False


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/commander', methods=['POST'])
def commander():
    nom = request.form.get('nom')
    telephone = request.form.get('telephone')
    supplement = request.form.get('supplement') or "Aucun"
    boisson = request.form.get('boisson') or "Aucune"
    quartier = request.form.get('quartier')
    quartier_autre = request.form.get('quartier_autre', '').strip()

    # Gestion du quartier final
    if quartier == "Autre" and quartier_autre:
        quartier_final = quartier_autre
        livraison = 1000  # Valeur par défaut si quartier inconnu
    elif quartier in frais_livraison:
        quartier_final = quartier
        livraison = frais_livraison[quartier]
    else:
        quartier_final = "Inconnu"
        livraison = 1000  # Valeur par défaut si erreur

    # Gestion de la quantité (avec erreur possible)
    try:
        quantite = int(request.form.get('quantite', '1'))
    except ValueError:
        quantite = 1

    # Récupère tous les plats sélectionnés
    plats_bruts = request.form.getlist('plats[]')

    # Nettoie les noms des plats en retirant le prix
    plats = []
    for plat in plats_bruts:
        clean_plat = plat.split(" -")[0].strip()
        if clean_plat:
            plats.append(clean_plat)

    # Récupère les accompagnements sélectionnés
    accompagnements_bruts = request.form.getlist('accompagnements[]')

    # Nettoie les noms des accompagnements
    accompagnements = []
    for acomp in accompagnements_bruts:
        clean_acompaniment = acomp.split(" -")[0].strip()
        if clean_acompaniment:
            accompagnements.append(clean_acompaniment)

    print("=== NOUVELLE COMMANDE ===")
    print(f"Nom : {nom}")
    print(f"Téléphone : {telephone}")
    print(f"Quartier : {quartier_final}")
    print(f"Frais de livraison : {livraison} FCFA")
    print(f"Plats : {', '.join(plats)}")
    print(f"Accompagnements : {', '.join(accompagnements)}")
    print(f"Quantité : {quantite}")
    print(f"Boisson : {boisson}")
    print(f"Informations supplémentaires : {supplement}")
    print("===========================")

    # Dictionnaire des prix des plats
    plats_prix = {
        "Bourgignon sauté à la moutarde": 4000,
        "Bourgignon sauté aux légumes avec le riz": 6000,
        "Soupe de carpe avec attiéké": 4000,
        "Soupe du pêcheur avec attiéké": 6000,
        "Poulet au gingembre": 3500,
        "Demi Poulet": 3500,
        "Demi Poulet Pané": 3500,
        "Kedjenou de Poulet": 3500,
        "Spaghetti au bourguignon": 4000,
        "Attieké Poisson sole frit": 2500,
        "Spaghetti aux boulettes": 4000,
        "Spaghetti au poulet": 4500,
        "Attieké poulet": 3000,
        "Ignames grillés au poisson": 4000,
        "Ragoût d'ignames au boeuf": 4500,
        "Ragoût d'ignames au poulet": 4500,
        "Petit Pois à la viande de bœuf": 4500,
        "Petit Pois aux boulettes": 4500,
        "Petit Pois au poulet": 4500,
        "Pomme de terre sautée au petit pois": 6500,
        "Pomme de terre sautée au bourguignon": 4500,
        "Soupe légumes maison": 3000,
        "Boulettes sautées": 4000,
        "Alloco aux oeufs": 2500,
        "Alloco au poulet": 3500,
        "frites aux Boulettes sautées": 4500,
        "frites au poulet sauté": 4000
    }

    # Calcul du total des plats
    total_plats = 0
    plats_avec_quantite = []

    for plat in plats:
        if plat in plats_prix:
            plat_prix = plats_prix[plat]
            total_plats += plat_prix * quantite
            plats_avec_quantite.append(f"{plat} x{quantite} = {plat_prix * quantite} FCFA")
        else:
            print(f"⚠️ Plat non reconnu : {plat}")

    # Calcul du total des accompagnements
    total_accompagnements = 0
    acompaniments_avec_quantite = []

    for acomp in accompagnements:
        if acomp in accompagnements_prix:
            acomp_prix = accompagnements_prix[acomp]
            total_accompagnements += acomp_prix * quantite
            acompaniments_avec_quantite.append(f"{acomp} x{quantite} = {acomp_prix * quantite} FCFA")
        else:
            print(f"⚠️ Accompagnement non reconnu : {acomp}")

    # Prix de la boisson
    if "Coca Cola" in boisson:
        prix_boisson = 500
    elif "Eau 1.5L" in boisson:
        prix_boisson = 1000
    else:
        prix_boisson = 0

    # Total général
    total = total_plats + total_accompagnements + livraison + prix_boisson

    # Prépare le message pour Telegram
    message = "*Nouvelle commande reçue !*\n\n"
    message += f"Client : {nom}\n"
    message += f"Téléphone : {telephone}\n\n"

    # Plats sélectionnés
    message += "Plats sélectionnés :\n"
    if plats_avec_quantite:
        message += "- " + "\n- ".join(plats_avec_quantite) + "\n\n"
    else:
        message += "Aucun plat sélectionné.\n\n"

    # Accompagnements sélectionnés
    if acompaniments_avec_quantite:
        message += "Accompagnements sélectionnés :\n"
        message += "- " + "\n- ".join(acompaniments_avec_quantite) + "\n\n"

    # Boisson
    message += f"Boisson : {boisson}\n\n"

    # Livraison
    message += f"Livraison ({quartier_final}) : {livraison} FCFA\n"

    # Total
    message += f"*Prix total : {total} FCFA*\n"

    # Informations supplémentaires
    message += f"Informations complémentaires : {supplement}"

    # Envoie à chaque chat ID Telegram
    send_telegram_message(message, TELEGRAM_CHAT_ID_1)
    
    if can_send_message(TELEGRAM_CHAT_ID_2):
        send_telegram_message(message, TELEGRAM_CHAT_ID_2)
    else:
        print("⚠️ Aucun message envoyé à TELEGRAM_CHAT_ID_2")

    return """
        <h2>Merci pour votre commande !</h2>
        <p>Nous vous contacterons bientôt.</p>
        <a href="/">Retour au menu</a>
    """


if __name__ == '__main__':
    import os
    if os.getenv("FLASK_ENV") == "production" or os.getenv("WERKZEUG_RUN_MAIN") == "true":
        from waitress import serve
        print("🚀 Démarrage en mode production avec Waitress")
        serve(app, host='0.0.0.0', port=8000)
    else:
        print("🔧 Démarrage en mode développement")
        app.run(debug=True, host='0.0.0.0', port=8000)