from flask import Flask, render_template, request, redirect, jsonify, session, url_for, send_file, make_response
from flask_mysqldb import MySQL
import io

app = Flask(__name__)
app.secret_key = 'supersecretkey'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/contactos')
def contactos():
    return render_template('contactos.html')

@app.route('/formularioespontaneo', methods=['GET', 'POST'])
def formularioespontaneo():
    if request.method == 'POST':
        nome = request.form['username']
        email = request.form['email']
        telefone = request.form['telefone']
        nacionalidade = request.form['nacionalidade']
        area = request.form['area-concorre']
        cv = request.files['CV'].read()

        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO t_candidaturaexpontanea (nome, email, telefone, Nacionalidade, area, cv)
            VALUES (%s,%s,%s,%s,%s,%s)
        """, (nome, email, telefone, nacionalidade, area, cv))

        mysql.connection.commit()
        cur.close()

        return redirect(url_for('home'))
    
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

@app.route('/detalhecandidatura/<int:candidatura_id>')
def detalhecandidatura(candidatura_id):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT id, nome, email, telefone, Nacionalidade, area, cv
        FROM t_candidaturaexpontanea
        WHERE id = %s
    """, (candidatura_id,))
    candidatura = cur.fetchone()
    cur.close()

    if candidatura is None:
        return "Candidatura não encontrada", 404

    return render_template('detalhecandidatura.html', candidatura = candidatura)

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
    cur = mysql.connection.cursor()
    cur.execute("Select id, nome, email, telefone, Nacionalidade, area FROM t_candidaturaexpontanea")
    candidaturas = cur.fetchall()
    cur.close()

    return render_template('candidaturasrecebidas.html', candidaturas = candidaturas)

@app.route('/pedidoscontacto')
def pedidoscontacto():
    return render_template('pedidoscontacto.html')

@app.route('/download_cv/<int:candidatura_id>')
def download_cv(candidatura_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT cv FROM t_candidaturaexpontanea WHERE id = %s", (candidatura_id,))
    resultado = cur.fetchone()
    cur.close()

    if resultado is None:
        return "Candidatura não encontrada", 404

    cv_data = resultado[0]

    if cv_data is None:
        return "CV não disponível", 404

    return send_file(
        io.BytesIO(cv_data),
        as_attachment=True,
        download_name="CV",
        mimetype='application/pdf'
    )

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'prosperabd'
app.config['MYSQL_UNIX_SOCKET'] = '/opt/lampp/var/mysql/mysql.sock'

mysql = MySQL(app)

if __name__ == '__main__':
    app.run(debug=True)

