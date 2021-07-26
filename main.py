import mysql.connector
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
import datetime
import jwt
from functools import wraps
import random
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret1234567890'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:admin@localhost/users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



#CRIAR TABELA USUARIO
class User(db.Model):
    __tablename__ = "usuarios"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(1000), nullable=False)

#CRIAR TABELA DE APOSTAS
class Game(db.Model):
    __tablename__ = "jogos"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    jogo = db.Column(db.String(80), unique=True, nullable=False)

db.create_all()


lista_aposta = []
final = []
token = None

#DECORATOR DA AUTENTICAÇÃO JWT (NÃO TERMINADO)
def jwt_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        global token

        print(token)
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']
        if not token:
            return jsonify({"error" : "Sem permissao para acessar essa rota"}), 401
        # if not "Bearer" in token:
        #     return jsonify({"Error": "Token Invalido"}), 401
        try:
            print(token)
            # token_pure = token.replace("Bearer", "")
            # print(token_pure)
            decoded = jwt.decode(token, app.config['SECRET_KEY'])
            print(decoded)
            current_user = User.query.filter_by(id=decoded['id']).first()
            print(current_user)
        except:
            return jsonify({"error" : "Token invalido"}), 401
        return f(current_user, *args, **kwargs)
    return wrapper


#ROTA PRINCIPAL
@app.route('/')
def home():
    return render_template('home.html')

#ROTA PARA LOGIN
@app.route('/login', methods=["GET", "POST"])
def login():

    if request.method == "POST":
        global token
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if not user:
            flash("Este usuário não existe. Tente novamente!")
            return redirect(url_for('login'))
        if not check_password_hash(user.password, password):
            flash("Senha Inválida! Tente novamente!")
            return redirect(url_for('login'))

        payload = {
            "id": user.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }
        token = jwt.encode(payload, app.config['SECRET_KEY'])

        return redirect(url_for('index'))
    return render_template('login.html')


#ROTA PARA REGISTARR USUÁRIO
@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":

        hashed_password = generate_password_hash(request.form.get("password"))

        new_user = User(username=request.form.get("username"),
                        password=hashed_password
                        )

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('register.html')

#ROTA PARA PÁGINA INDEX APÓS LOGAR
@app.route('/index')
# @jwt_required
def index():
    return render_template('index.html')

#ROTA PARA DESCONECTAR USUARIO (AUTENTICAÇÃO NÃO TERMINADA)
@app.route('/logout')
# @jwt_required
def logout():
    return redirect(url_for('home'))

#ROTA PARA EDITAR USUARIO E SENHA
@app.route('/update', methods=["GET", "POST"])
# @jwt_required
def update():
    global token
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(username=username).first()

        if not user:
            flash("Este usuário não existe. Tente novamente!")
            return redirect(url_for('login'))
        if not check_password_hash(user.password, password):
            flash("Senha Inválida! Tente novamente!")
            return redirect(url_for('login'))

        payload = {
            "id": user.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }
        token = jwt.encode(payload, app.config['SECRET_KEY'])

        hashed_password = generate_password_hash(request.form.get("password"))
        new_username = request.form.get("new_username")
        new_password = hashed_password

        con = mysql.connector.connect(host="localhost", user="admin", password="admin", db="users")
        cur = con.cursor()
        update = cur.execute(f"UPDATE usuarios SET username = '{new_username}', password = '{new_password}' WHERE username = '{username}';")
        cur.execute(update)
        con.commit()

        flash("Edição Realizada com Sucesso!")
    return render_template('update.html')

#ROTA PARA DELETAR USUARIO
@app.route('/delete', methods=["GET", "POST"])
# @jwt_required
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
            delete = cur.execute(f"DELETE FROM usuarios WHERE username = '{username}';")
            cur.execute(delete)
            con.commit()
            flash("Usuário Deletado")
            return redirect(url_for('home'))
    return render_template('delete.html')

#ROTA PARA MOSTRAR ACERTOS NA APOSTA
@app.route('/hits')
# @jwt_required
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


#ROTA PARA MOSTRAR ULTIMO RESULTADO DA MEGA-SENA
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

#ROTA PARA CRIAR UM NOVO JOGO
@app.route('/new', methods=["GET", "POST"])
# @jwt_required
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

#ROTA PARA LISTAR TODAS AS APOSTAS
@app.route("/list")
# @jwt_required
def get_all_games():
    con = mysql.connector.connect(host="localhost", user="admin", password="admin", db="users")
    cur = con.cursor()
    cur.execute("SELECT jogo from jogos ORDER BY id ASC;")
    games = cur.fetchall()
    return render_template("list.html", games=games)

if __name__ == "__main__":
    app.run(debug=True)