from flask import Flask, render_template, request, send_from_directory

app = Flask(__name__, static_folder='static', template_folder='templates')

# Route pour servir les fichiers statiques (au cas où Flask ne le fait pas tout seul)
@app.route('/style.css')
def style_css():
    return send_from_directory('static', 'style.css')

# Route principale
@app.route('/')
def index():
    return render_template('index.html')

# Route pour recevoir les commandes
@app.route('/commander', methods=['POST'])
def commander():
    nom = request.form.get('nom')
    plat = request.form.get('plat')
    quantite = request.form.get('quantite')
    telephone = request.form.get('telephone')

    print(f"Nouvelle commande reçue !")
    print(f"Nom: {nom} | Plat: {plat} | Quantité: {quantite} | Téléphone: {telephone}")

    return """
        <h2>Merci pour votre commande !</h2>
        <p>Nous vous contacterons bientôt.</p>
        <a href="/">Retour au menu</a>
    """

# Pour exécuter localement avec waitress
if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=8000)