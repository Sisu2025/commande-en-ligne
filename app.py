from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

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

if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=8000)