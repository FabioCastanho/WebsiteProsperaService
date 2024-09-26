from flask import Flask, render_template, request, redirect, url_for, send_file, session, abort
from flask_mysqldb import MySQL
import io
from functools import wraps

app = Flask(__name__)
app.secret_key = 'supersecretkey'

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('loginadmin'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/contactos', methods=['GET', 'POST'])
def contactos():
    if request.method == 'POST':
        nome_contacto = request.form['nome-contacto']
        nome_empresa = request.form['nome-empresa']
        email = request.form['email']
        telefone = request.form['telefone']
        area_atividade = request.form['area-atividade']
        mensagem = request.form['message']
        
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO t_pedido (nome_contacto, nome_empresa, email, telefone, area_actividade, mensagem)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (nome_contacto, nome_empresa, email, telefone, area_atividade, mensagem))
        mysql.connection.commit()
        cur.close()

        return render_template('contactos.html', success=True)

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

@app.route('/vagas', methods=['GET'])
def vagas():
    search = request.args.get('search', '')
    location = request.args.get('location', '')
    job_type = request.args.get('jobType', '')

    query = "SELECT * FROM t_vaga WHERE 1=1"
    params = []

    if search:
        query += " AND (titulo LIKE %s OR area LIKE %s)"
        params.extend(['%' + search + '%', '%' + search + '%'])

    if location:
        query += " AND localizacao = %s"
        params.append(location)

    if job_type:
        query += " AND tipo_contrato = %s"
        params.append(job_type)

    cur = mysql.connection.cursor()
    cur.execute(query, params)
    vagas = cur.fetchall()
    cur.close()

    return render_template('vagas.html', vagas=vagas)


@app.route('/admin')
@login_required
def admin():
    return render_template('admin.html')

@app.route('/criarvaga', methods=['GET', 'POST'])
def criarvaga():
    if request.method == 'POST':
        titulo = request.form['titulo']
        area = request.form['area']
        descricao = request.form['descricao']
        requisitos = request.form['requisitos']
        beneficios = request.form['beneficios']
        localizacao = request.form['localizacao']
        tipo_contrato = request.form['tipo_contrato']
        area = request.form['area']

        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO t_vaga (titulo, area, descricao, requisitos, beneficios, localizacao, tipo_contrato)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (titulo, area, descricao, requisitos, beneficios, localizacao, tipo_contrato))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('criarvaga'))

    return render_template('criarvaga.html')


@app.route('/loginadmin')
def loginadmin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == 'admin' and password == 'pass':  
            session['user_id'] = username  
            return redirect(url_for('admin'))
        else:
            return "Login inválido", 401

    return render_template('loginadmin.html')

@app.route('/detalhecandidatura/<int:candidatura_id>')
@login_required
def detalhecandidatura(candidatura_id):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT 'espontanea' AS tipo, id, nome, email, telefone, Nacionalidade, area, cv
        FROM t_candidaturaexpontanea
        WHERE id = %s
    """, (candidatura_id,))

    candidatura = cur.fetchone()
    cur.close()

    if candidatura is None:
        return "Candidatura não encontrada", 404

    return render_template('detalhecandidatura.html', candidatura = candidatura)

@app.route('/detalhecandidaturavaga/<int:candidatura_id>')
@login_required
def detalhecandidaturavaga(candidatura_id):
    cur = mysql.connection.cursor()

    cur.execute("""
        SELECT c.id, c.nome, c.email, c.telefone, c.cv, v.titulo AS nome_vaga
        FROM t_candidaturavaga c
        JOIN t_vaga v ON c.id_vaga = v.id
        WHERE c.id = %s
    """, (candidatura_id,))
    
    candidatura = cur.fetchone()
    cur.close()

    if candidatura is None:
        return "Candidatura não encontrada", 404

    return render_template('detalhecandidatura.html', candidatura=candidatura)



@app.route('/detalhepedido/<int:pedido_id>')
@login_required
def detalhepedido(pedido_id):
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT id, nome_contacto, nome_empresa, email, telefone, area_actividade, mensagem 
        FROM t_pedido
        WHERE id = %s
    """, (pedido_id,))
    pedido = cur.fetchone()
    cur.close()

    if pedido is None:
        return "Pedido não encontrada", 404

    return render_template('detalhepedido.html', pedido = pedido)

@app.route('/detalhevaga/<int:vaga_id>', methods=['GET'])
def detalhevaga(vaga_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM t_vaga WHERE id = %s", (vaga_id,))
    vaga = cur.fetchone()
    cur.close()

    if vaga:
        return render_template('detalhevaga.html', vaga=vaga)
    else:
        return "Vaga não encontrada", 404


@app.route('/formulariovaga/<int:vaga_id>', methods=['GET', 'POST'])
def formulariovaga(vaga_id):
    if request.method == 'POST':
        nome = request.form['username']
        email = request.form['email']
        telefone = request.form['telefone']
        nacionalidade = request.form['nacionalidade']
        cv = request.files['CV'].read()

        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO t_candidaturavaga (nome, email, telefone, Nacionalidade, cv, id_vaga)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (nome, email, telefone, nacionalidade, cv, vaga_id))

        mysql.connection.commit()
        cur.close()

        return redirect(url_for('vagas'))

    return render_template('formulariovaga.html', vaga_id=vaga_id)


@app.route('/candidaturasrecebidas', methods=['GET'])
@login_required
def candidaturasrecebidas():
    location = request.args.get('location', '')
    job_type = request.args.get('jobType', '')
    search = request.args.get('search', '')
    tipo_candidatura = request.args.get('tipo_candidatura', 'todas')  

    query_espontanea = """
        SELECT 'espontanea' AS tipo, id, nome, email, telefone, Nacionalidade, area, NULL AS vaga_titulo 
        FROM t_candidaturaexpontanea
        WHERE 1=1
    """
    
    query_vaga = """
        SELECT 'vaga' AS tipo, cv.id, cv.nome, cv.email, cv.telefone, cv.Nacionalidade, v.area, v.titulo AS vaga_titulo
        FROM t_candidaturavaga cv
        JOIN t_vaga v ON cv.id_vaga = v.id
        WHERE 1=1
    """

    params = []

    if search:
        query_espontanea += " AND (nome LIKE %s)"
        query_vaga += " AND (cv.nome LIKE %s)"
        params.extend(['%' + search + '%', '%' + search + '%'])

    if location:
        query_espontanea += " AND (Nacionalidade = %s)"
        query_vaga += " AND (cv.Nacionalidade = %s)"
        params.append(location)

    if job_type:
        query_vaga += " AND (v.tipo_contrato = %s)"
        params.append(job_type)

    if tipo_candidatura == 'espontanea':
        query = query_espontanea
    elif tipo_candidatura == 'vaga':
        query = query_vaga
    else:
        query = f"{query_espontanea} UNION {query_vaga}"

    cur = mysql.connection.cursor()
    cur.execute(query, params)
    candidaturas = cur.fetchall()
    cur.close()

    return render_template('candidaturasrecebidas.html', candidaturas=candidaturas)


@app.route('/pedidoscontacto')
@login_required
def pedidoscontacto():
    search_query = request.args.get('search', '') 

    cur = mysql.connection.cursor()

    if search_query:
        query = """
            SELECT id, nome_contacto, nome_empresa, email, telefone, area_actividade, mensagem 
            FROM t_pedido 
            WHERE nome_empresa LIKE %s OR area_actividade LIKE %s
        """
        search_term = f"%{search_query}%"  
        cur.execute(query, (search_term, search_term))
    else:
        cur.execute("SELECT id, nome_contacto, nome_empresa, email, telefone, area_actividade, mensagem FROM t_pedido")

    pedidos = cur.fetchall()
    cur.close()

    return render_template('pedidoscontacto.html', pedidos=pedidos)


@app.route('/download_cv/<int:candidatura_id>')
@login_required
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
        download_name="CV.pdf",
        mimetype='application/pdf'
    )

@app.route('/download_cv_vaga/<int:candidatura_id>')
@login_required
def download_cv_vaga(candidatura_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT cv FROM t_candidaturavaga WHERE id = %s", (candidatura_id,))
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
        download_name="CV_Vaga.pdf",
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

