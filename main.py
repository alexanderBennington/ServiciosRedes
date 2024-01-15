from flask import Flask, render_template, request, redirect, url_for
import paramiko, time
import subprocess

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
    elif router == '5':
        ip = '192.1.1.18'
        return ip
    elif router == '6':
        ip = '209.165.200.226'
        return ip
    else:
        ip = 'Error no se ha seleccionado algun router'
        return ip

@app.route('/seleccion', methods=['POST'])
def seleccion():
    protocolo = request.form.get('protocolo')
    router = request.form.get('router')
    ip = iprouter(router)
    if protocolo == 'ACL':
        resultado = ACL(ip)
    elif protocolo == 'DHCP':
        resultado = DHCP(ip)
    elif protocolo == 'NAT':
        resultado = NAT(ip)
    elif protocolo == 'DNS':
        resultado = DNS(ip)
    elif protocolo == 'VPN':
        resultado = VPN(ip)
    elif protocolo == 'SNMP':
        resultado = SNMP(ip)
    elif protocolo == 'RMON':
        resultado = RMON(ip)
    elif protocolo == 'VLAN':
        resultado = VLAN(ip)
    elif protocolo == 'PROTOCOLO':
        resultado = PROTOCOLO(ip)
    else:
        resultado = ip + "no mano"
    return render_template('protocolos.html', resultado=resultado, router=router)

@app.route('/comando', methods=['POST'])
def comando():
    tipo = request.form.get('tipo')
    interface = request.form.get('interface')
    comando = request.form.get('comando')
    router = request.form.get('router-comando')
    ip = iprouter(router)
    if tipo == 'normal':
        resultado = linea(ip, comando)
    elif tipo == 'acl':
        resultado = comando_acl(ip, interface, comando)
    return render_template('protocolos.html', resultado=resultado, router=router)

@app.route('/snmpd', methods=['POST'])
def snmpd():
    snmp = request.form.get('snmp')
    oid = request.form.get('oid')
    instruccion = request.form.get('instruccion')
    router = request.form.get('router-snmp')
    if instruccion is None or instruccion.strip() == "":
        instruccion = " "
    if oid is None or oid.strip() == "":
        oid = " "
    ip = iprouter(router)
    consulta = snmp + ' -v3 -a sha -A cisco123 -x des -X cisco123 -l authpriv -u cisco ' + ip + " " + oid + " " + instruccion
    resultado_consulta = subprocess.run(consulta, shell=True, capture_output=True, text=True)
    if resultado_consulta.returncode != 0:
        resultado = "Error al ejecutar comando. Código de salida: ", resultado_consulta.returncode
    else:
        resultado = resultado_consulta.stdout
    return render_template('protocolos.html', resultado=resultado, router=router)

def ACL(ip):
    try:
        ssh_cliente = paramiko.SSHClient()
        ssh_cliente.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_cliente.connect(hostname = ip, username = correct_username, password = correct_password)
        
        shell = ssh_cliente.invoke_shell()
        time.sleep(1)
        shell.send('show access-lists\n')
        time.sleep(5)
        salida = shell.recv(65535).decode('ascii')
        return "Conexion realizada con exito!\n" + salida
    except Exception as e:
        return "Error: " + str(e)
def DHCP(ip):
    try:
        ssh_cliente = paramiko.SSHClient()
        ssh_cliente.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_cliente.connect(hostname = ip, username = correct_username, password = correct_password)
        
        shell = ssh_cliente.invoke_shell()
        time.sleep(1)
        shell.send('show running-config | include dhcp pool\n')
        time.sleep(1)
        shell.send('show ip dhcp binding\n')
        time.sleep(1)
        shell.send('show ip dhcp server statistics\n')
        time.sleep(5)
        salida = shell.recv(65535).decode('ascii')
        return "Conexion realizada con exito!\n" + salida
    except Exception as e:
        return "Error: " + str(e)
def NAT(ip):
    try:
        ssh_cliente = paramiko.SSHClient()
        ssh_cliente.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_cliente.connect(hostname = ip, username = correct_username, password = correct_password)
        
        shell = ssh_cliente.invoke_shell()
        time.sleep(1)
        shell.send('show running-config | include nat\n')
        time.sleep(1)
        shell.send('show ip nat translations\n')
        time.sleep(1)
        shell.send('show ip nat statistics\n')
        time.sleep(5)
        salida = shell.recv(65535).decode('ascii')
        return "Conexion realizada con exito!\n" + salida
    except Exception as e:
        return "Error: " + str(e)
def DNS(ip):
    try:
        ssh_cliente = paramiko.SSHClient()
        ssh_cliente.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_cliente.connect(hostname = ip, username = correct_username, password = correct_password)
        
        shell = ssh_cliente.invoke_shell()
        time.sleep(1)
        shell.send('show running-config | include dns\n')
        time.sleep(1)
        shell.send('show hosts\n')
        time.sleep(1)
        shell.send('show ip domain\n')
        time.sleep(5)
        salida = shell.recv(65535).decode('ascii')
        return "Conexion realizada con exito!\n" + salida
    except Exception as e:
        return "Error: " + str(e)
def VPN(ip):
    try:
        ssh_cliente = paramiko.SSHClient()
        ssh_cliente.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_cliente.connect(hostname = ip, username = correct_username, password = correct_password)
        
        shell = ssh_cliente.invoke_shell()
        time.sleep(1)
        shell.send('show running-config | include crypto\n')
        time.sleep(1)
        shell.send('show crypto isakmp sa\n')
        time.sleep(1)
        shell.send('show crypto ipsec sa\n')
        time.sleep(1)
        shell.send('show crypto map\n')
        time.sleep(1)
        shell.send('show crypto dynamic-map\n')
        time.sleep(5)
        salida = shell.recv(65535).decode('ascii')
        return "Conexion realizada con exito!\n" + salida
    except Exception as e:
        return "Error: " + str(e)
def SNMP(ip):
    try:
        ssh_cliente = paramiko.SSHClient()
        ssh_cliente.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_cliente.connect(hostname = ip, username = correct_username, password = correct_password)
        
        shell = ssh_cliente.invoke_shell()
        time.sleep(1)
        shell.send('show snmp user\n')
        time.sleep(1)
        shell.send('show snmp group\n')
        time.sleep(1)
        shell.send('show snmp view\n')
        time.sleep(5)
        salida = shell.recv(65535).decode('ascii')
        return "Conexion realizada con exito!\n" + salida
    except Exception as e:
        return "Error: " + str(e)
def RMON(ip):
    try:
        ssh_cliente = paramiko.SSHClient()
        ssh_cliente.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_cliente.connect(hostname = ip, username = correct_username, password = correct_password)
        
        shell = ssh_cliente.invoke_shell()
        time.sleep(1)
        shell.send('show rmon\n')
        time.sleep(1)
        shell.send('show rmon event\n')
        time.sleep(5)
        salida = shell.recv(65535).decode('ascii')
        return "Conexion realizada con exito!\n" + salida
    except Exception as e:
        return "Error: " + str(e)
def VLAN(ip):
    try:
        ssh_cliente = paramiko.SSHClient()
        ssh_cliente.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_cliente.connect(hostname = ip, username = correct_username, password = correct_password)
        
        shell = ssh_cliente.invoke_shell()
        time.sleep(1)
        shell.send('show running-config interface fa0/0\n')
        time.sleep(5)
        salida = shell.recv(65535).decode('ascii')
        return "Conexion realizada con exito!\n" + salida
    except Exception as e:
        return "Error: " + str(e)
def PROTOCOLO(ip):
    try:
        ssh_cliente = paramiko.SSHClient()
        ssh_cliente.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_cliente.connect(hostname = ip, username = correct_username, password = correct_password)
        
        shell = ssh_cliente.invoke_shell()
        time.sleep(1)
        shell.send('show running-config | section router ospf\n')
        time.sleep(1)
        shell.send('show ip route\n')
        time.sleep(1)
        shell.send(' \n')
        time.sleep(1)
        shell.send('show ip int br\n')
        time.sleep(5)
        salida = shell.recv(65535).decode('ascii')
        return "Conexion realizada con exito!\n" + salida
    except Exception as e:
        return "Error: " + str(e)
def linea(ip, comando):
    try:
        ssh_cliente = paramiko.SSHClient()
        ssh_cliente.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_cliente.connect(hostname = ip, username = correct_username, password = correct_password)
        
        shell = ssh_cliente.invoke_shell()
        time.sleep(1)
        shell.send(comando + '\n')
        time.sleep(5)
        salida = shell.recv(65535).decode('ascii')
        return "Conexion realizada con exito!\n" + salida
    except Exception as e:
        return "Error: " + str(e)
def comando_acl(ip, interface, comando):
    try:
        ssh_cliente = paramiko.SSHClient()
        ssh_cliente.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_cliente.connect(hostname = ip, username = correct_username, password = correct_password)
        
        shell = ssh_cliente.invoke_shell()
        time.sleep(1)
        shell.send('conf term\n')
        time.sleep(1)
        shell.send(interface + '\n')
        time.sleep(1)
        shell.send(comando + '\n')
        time.sleep(1)
        shell.send('end\n')
        time.sleep(5)
        salida = shell.recv(65535).decode('ascii')
        return "Conexion realizada con exito!\n" + salida
    except Exception as e:
        return "Error: " + str(e)

if __name__ == '__main__':
    app.run(debug=True)

#snmpwalk -v3 -a sha -A cisco123 -x des -X cisco123 -l authpriv -u cisco 192.1.1.13 1.3.6.1.2.1.4.20.1.1