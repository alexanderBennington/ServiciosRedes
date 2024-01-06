from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

correct_username = "cisco"
correct_password = "cisco"

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('usuario')
    password = request.form.get('clave')

    if username == correct_username and password == correct_password:
        return redirect(url_for('topologia'))
    else:
        error = 'Credenciales incorrectas. Inténtalo de nuevo.'
        return render_template('index.html', error=error)

@app.route('/topologia')
def topologia():
    return render_template('topologia.html')

@app.route('/protocolos/<router>')
def protocolos(router):
    return render_template('protocolos.html', router=router)

if __name__ == '__main__':
    app.run(debug=True)