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

def iprouter(router):
    if router == '1':
        ip = '192.1.1.2'
        return ip
    elif router == '2':
        ip = '192.1.1.1'
        return ip
    elif router == '3':
        ip = '192.1.1.5'
        return ip
    elif router == '4':
        ip = '192.1.1.13'
        return ip
    else:
        ip = 'Error no se ha seleccionado algun router'
        return ip

@app.route('/seleccion', methods=['POST'])
def seleccion():
    protocolo = request.form.get('protocolo')
    router = request.form.get('router')
    ip = iprouter(router)
    if protocolo == 'DHCP':
        resultado = DHCP(ip)
    else:
        resultado = ip + "no mano"
    return render_template('protocolos.html', resultado=resultado, router=router)


def DHCP(ip):
    return ip


if __name__ == '__main__':
    app.run(debug=True)