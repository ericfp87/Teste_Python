from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    return render_template('login.html')

@app.route('/register', methods=["GET", "POST"])
def register():
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