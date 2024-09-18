from flask import Flask, render_template, request, redirect, jsonify, session, url_for
from flask_mysqldb import MySQL
from bson.binary import Binary

app = Flask(__name__)
app.secret_key = 'supersecretkey'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/contactos')
def contactos():
    return render_template('contactos.html')

@app.route('/formularioespontaneo')
def formularioespontaneo():
    return render_template('formularioespontaneo.html')

@app.route('/sobrenos')
def sobrenos():
    return render_template('sobrenos.html')

@app.route('/servicos')
def servicos():
    return render_template('servicos.html')

@app.route('/vagas')
def vagas():
    return render_template('vagas.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/criarvaga')
def criarvaga():
    return render_template('criarvaga.html')

@app.route('/loginadmin')
def loginadmn():
    return render_template('loginadmin.html')

@app.route('/detalhecandidatura')
def detalhecandidatura():
    return render_template('detalhecandidatura.html')

@app.route('/detalhepedido')
def detalhepedido():
    return render_template('detalhepedido.html')

@app.route('/detalhevaga')
def detalhevaga():
    return render_template('detalhevaga.html')

@app.route('/formulariovaga')
def formulariovaga():
    return render_template('formulariovaga.html')

@app.route('/candidaturasrecebidas')
def candidaturasrecebidas():
    return render_template('candidaturasrecebidas.html')

@app.route('/pedidoscontacto')
def pedidoscontacto():
    return render_template('pedidoscontacto.html')

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'ProsperaBD'
app.config['MYSQL_UNIX_SOCKET'] = '/opt/lampp/var/mysql/mysql.sock'

mysql = MySQL(app)

if __name__ == '__main__':
    app.run(debug=True)

