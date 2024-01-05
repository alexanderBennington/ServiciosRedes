from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

correct_username = "usuario"
correct_password = "clave"

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('usuario')
    password = request.form.get('clave')

    if username == correct_username and password == correct_password:
        return redirect(url_for('principal'))
    else:
        error = 'Credenciales incorrectas. Inténtalo de nuevo.'
        return render_template('index.html', error=error)

@app.route('/principal')
def principal():
    return render_template('principal.html')

if __name__ == '__main__':
    app.run(debug=True)