@app.route('/commander', methods=['POST'])
def commander():
    nom = request.form.get('nom')
    telephone = request.form.get('telephone')
    supplement = request.form.get('supplement') or "Aucun"
    boisson = request.form.get('boisson') or "Aucune"

    # Gestion de la quantité
    try:
        quantite = int(request.form.get('quantite', '1'))
    except ValueError:
        quantite = 1

    # Récupération des plats
    plats_bruts = request.form.getlist('plats[]')

    # Nettoyage des noms de plat
    plats = []
    for plat in plats_bruts:
        clean_plat = plat.split(" -")[0].strip()
        if clean_plat:
            plats.append(clean_plat)

    print("=== NOUVELLE COMMANDE ===")
    print(f"Nom : {nom}")
    print(f"Téléphone : {telephone}")
    print(f"Plats : {', '.join(plats)}")
    print(f"Quantité : {quantite}")
    print(f"Boisson : {boisson}")
    print(f"Informations complémentaires : {supplement}")
    print("===========================")

    # Dictionnaire des prix
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
        "Ragoût d'i pour gnames au boeuf": 4500,
        "Ragoût d'i pour gnames au poulet": 4500,
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
        "frites au poulet sauté": 4000,
        "Attieké huile rouge": 630,
        "Riz": 1000,
        "Claclo": 1000,
        "Alloco": 1000,
        "Ignames grillés": 1000
    }

    # Calcul du total
    total = 0
    plats_avec_quantite = []

    for plat in plats:
        if plat in plats_prix:
            plat_prix = plats_prix[plat]
            total += plat_prix * quantite
            plats_avec_quantite.append(f"{plat} x{quantite} = {plat_prix * quantite} FCFA")
        else:
            print(f"⚠️ Plat non reconnu : {plat}")

    # Envoi Telegram
    message = "*Nouvelle commande reçue !*\n\n"
    message += f"Client : {nom}\n"
    message += f"Téléphone : {telephone}\n\n"
    message += "Plats sélectionnés :\n"
    message += "- " + "\n- ".join(plats_avec_quantite) + "\n\n"
    message += f"*Prix total : {total} FCFA*\n"
    message += f"Boisson : {boisson}\n"
    message += f"Informations complémentaires : {supplement}"

    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage" 
        data = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "Markdown"
        }
        response = requests.post(url, data=data)
        if response.status_code == 200 and response.json().get("ok"):
            print("✅ Message envoyé via Telegram")
        else:
            print("❌ Échec d'envoi Telegram", response.json())
    except Exception as e:
        print("🚨 Erreur lors de l'envoi Telegram :", str(e))

    return """
        <h2>Merci pour votre commande !</h2>
        <p>Nous vous contacterons bientôt.</p>
        <a href="/">Retour au menu</a>
    """