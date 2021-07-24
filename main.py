from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SECRET_KEY'] = 'secret1234567890'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:admin@localhost/users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = "usuarios"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)



db.create_all()


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

        else:
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

        return redirect(url_for('index'))


    return render_template('register.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/logout')
def logout():
    return redirect(url_for('home'))

@app.route('/update', methods=["GET", "PATCH"])
def update():
    return render_template('update.html')

@app.route('/delete', methods=["GET", "DELETE"])
def delete():
    pass

@app.route('/hits')
def hits():
    return render_template('hits.html')

@app.route('/result')
def result():
    return render_template('last_mega.html')

@app.route('/new', methods=["GET", "POST"])
def new_game():
    return render_template('new_game.html')

if __name__ == "__main__":
    app.run(debug=True)