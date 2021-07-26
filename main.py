import mysql.connector
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, redirect, url_for, request, flash, jsonify, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
import datetime
import jwt
from flask_login import login_user
from functools import wraps
import random
import webScraping_MegaSena

# from app import app, db


app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret1234567890'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:admin@localhost/users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma = Marshmallow(app)
Migrate(app, db)


class User(db.Model):
    __tablename__ = "usuarios"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

class Game(db.Model):
    __tablename__ = "jogos"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    jogo = db.Column(db.String(80), unique=True, nullable=False)

db.create_all()


lista_aposta = []
final = []

def jwt_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.args.get('token')

        if not token:
            return jsonify({"error" : "Sem permissão para acessar essa rota"}), 403
        if not "Bearer" in token:
            return jsonify({"Token Inválido"}), 401
        try:
            token_pure = token.replace("Bearer", "")
            decoded = jwt.decode(token_pure, current_app.config['SECRET_KEY'])
            current_user = User.query.get(username=decoded['username'])
        except:
            return jsonify({"error" : "Token inválido"}), 403
        return f(current_user=current_user, *args, **kwargs)
    return wrapper

@app.shell_context_processor
def make_shell_context():
    return dict (
        app=app,
        db=db,
        User=User
    )

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()
        pwd = User.query.filter_by(password=password).first()
        if not user:
            flash("Este usuário não existe. Tente novamente!")
            return redirect(url_for('login'))
        elif not pwd:
            flash("Senha Inválida! Tente novamente!")
            return redirect(url_for('login'))

        payload = {
            "id": user.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }
        token = jwt.encode(payload, app.config['SECRET_KEY'])

        return redirect(url_for('index'))
    return render_template('login.html')



@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":

        new_user = User(username=request.form.get("username"),
                        password=request.form.get("password")
                        )

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/logout')
def logout():
    return redirect(url_for('home'))

@app.route('/update', methods=["GET", "PATCH"])
@jwt_required
def update():
    return render_template('update.html')

@app.route('/delete', methods=["GET", "POST"])
def delete():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()
        pwd = User.query.filter_by(password=password).first()
        if not user:
            flash("Este usuário não existe. Tente novamente!")
            return redirect(url_for('login'))

        elif not pwd:
            flash("Senha Inválida! Tente novamente!")
            return redirect(url_for('login'))

        else:
            con = mysql.connector.connect(host="localhost", user="admin", password="admin", db="users")
            cur = con.cursor()
            cur.execute(f"DELETE FROM usuarios WHERE username = {username};")
            games = cur.fetchall()
            return redirect(url_for('home'))
    return render_template('delete.html')


@app.route('/hits')
def hits():
    URL = "https://www.google.com/search?q=caixa+mega+sena"


    del final[:]
    resposta = requests.get(URL, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'})
    soup = BeautifulSoup(resposta.content)
    numeros_finais = soup.find_all("span", {"class": "zSMazd UHlKbe"})
    for numero in numeros_finais:
        final.append(numero.text)

    for i in range(0, len(final)):
        final[i] = int(final[i])
    print(final)

    diff_acertos = list(set(lista_aposta) - set(final))
    print(diff_acertos)
    acertos = len(lista_aposta) - len(diff_acertos)
    print(acertos)
    return render_template('hits.html', acertos=acertos)



@app.route('/result')
def result():
    URL = "https://www.google.com/search?q=caixa+mega+sena"

    final = []
    resposta = requests.get(URL, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'})
    soup = BeautifulSoup(resposta.content)
    numeros_finais = soup.find_all("span", {"class": "zSMazd UHlKbe"})
    for numero in numeros_finais:
        final.append(numero.text)
    print(final)
    return render_template('last_mega.html', final=final)

@app.route('/new', methods=["GET", "POST"])

def new_game():
    if request.method == "POST":

        qtd = int(request.form.get("qtd"))
        if qtd > 5 and qtd < 11:
            aposta = random.sample(range(1, 61), qtd)
            del lista_aposta[:]
            for num in aposta:
                lista_aposta.append(num)
            list_db = str(lista_aposta)
            nova_aposta = Game(
                jogo=list_db
            )

            db.session.add(nova_aposta)
            db.session.commit()
            print(lista_aposta)
            print(qtd)
            print(aposta)
            return redirect(url_for('get_all_games'))
        else:
            flash("Escolha entre 6 a 10 numeros")
            print("numero errado")

    return render_template('new_game.html')

@app.route("/list")
def get_all_games():
    con = mysql.connector.connect(host="localhost", user="admin", password="admin", db="users")
    cur = con.cursor()
    cur.execute("SELECT jogo from jogos ORDER BY id ASC;")
    games = cur.fetchall()
    return render_template("list.html", games=games)

if __name__ == "__main__":
    app.run(debug=True)