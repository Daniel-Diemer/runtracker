from flask import Flask, render_template, request, redirect, url_for, flash, session
from database import atualizar_treino, buscar_treino_por_id, excluir_treino as excluir_treino_bd, criar_usuario, buscar_usuario_por_email, criar_treino, listar_treinos_usuario, buscar_resumo_treinos_usuario
from werkzeug.security import generate_password_hash, check_password_hash
from utils import formatar_distancia, verificar_senha, formatar_data, formatar_tempo, calcular_pace, transformar_tempo_em_segundos
import os 
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/dashboard")
def dashboard():
    if "usuario_id" not in session:
        flash("Faça login para acessar essa pagina","warning")
        return redirect(url_for("login"))

    nome_usuario = session["usuario_nome"]
    usuario_id = session["usuario_id"]

    resumo = buscar_resumo_treinos_usuario(usuario_id)
    total_treinos = resumo[0]
    total_km_numero = resumo[1]
    total_km = formatar_distancia(total_km_numero)
    total_segundos = resumo[2]
    tempo_total = formatar_tempo(total_segundos)

    if total_km_numero>0:
        pace_medio = calcular_pace(total_segundos, total_km_numero) +"/km"
    else:
        pace_medio = "Sem dados"


    return render_template("dashboard.html", nome_usuario=nome_usuario, total_km=total_km, tempo_total=tempo_total, total_treinos=total_treinos, pace_medio=pace_medio)
 

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"].strip()  # Serve para Apagar espaços no inicio e fim de uma string
        senha = request.form["senha"] 

        if not senha: 
            flash("Favor, digite sua senha", "error")
            return redirect(url_for("login"))

        if not email: 
            flash("Favor, digite seu email", "error")
            return redirect(url_for("login"))
        
        usuario = buscar_usuario_por_email(email)

        if not usuario:
            flash("E-mail não encontrado", "error")
            return redirect (url_for("login"))

        senha_hash = usuario[3]
        if not check_password_hash(senha_hash, senha):
            flash("Senha Incorreta", "error")
            return redirect (url_for("login"))

        flash("Login realizado com sucesso", "success")
        session["usuario_id"] = usuario[0]
        session["usuario_nome"] = usuario[1]
        return redirect (url_for("dashboard"))
        
    return render_template("login.html")

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form["nome"].strip()
        email = request.form["email"].strip()
        senha = request.form["senha"]
        confirmar_senha = request.form["confirmar_senha"]

        if not nome: 
            flash("Digite seu nome", "error")
            return redirect (url_for("cadastro"))

        if not email: 
            flash("Digite seu e-mail", "error")
            return redirect (url_for("cadastro"))

        if not senha:
            flash("Digite sua senha", "error")
            return redirect (url_for("cadastro"))

        if not confirmar_senha:
            flash("Confirme sua senha", "error")
            return redirect (url_for("cadastro"))

        if senha != confirmar_senha:
            flash("As senhas são diferentes", "error")
            return redirect(url_for("cadastro"))

        senha_valida, mensagem = verificar_senha(senha)
        
        if not senha_valida:
            flash(mensagem, "error")
            return redirect(url_for("cadastro"))


        usuario = buscar_usuario_por_email(email)
        
        if usuario:
            flash("E-mail já cadastrado", "error")
            return redirect (url_for("cadastro"))

        senha_hash = generate_password_hash(senha)
        criar_usuario(nome, email, senha_hash)
        flash("Cadastro realizado com sucesso", "success")
        return redirect(url_for("login"))

    return render_template("cadastro.html")

@app.route("/novo-treino", methods=["GET", "POST"])
def novo_treino():
    if "usuario_id" not in session:
        flash("Faça login para acessar essa pagina","warning")
        return redirect(url_for("login"))

    if request.method == "POST":
        data_treino = request.form["data_treino"]
        tipo = request.form["tipo"]
        distancia_km = request.form["distancia_km"]
        tempo = request.form["tempo"]
        observacao = request.form["observacao"]
        usuario_id = session["usuario_id"]

        if not data_treino:
            flash("Informe a data do treino", "error")
            return redirect(url_for("novo_treino"))

        if tipo not in ["corrida", "caminhada"]:
            flash("Tipo de treino inválido", "error")
            return redirect(url_for("novo_treino"))
        
        try:
            tempo_segundos = transformar_tempo_em_segundos(tempo)
        except ValueError as erro:
            flash(str(erro), "error")
            return redirect(url_for("novo_treino"))
        
        try:
            distancia_km = float(distancia_km.replace(",", "."))
        except ValueError:
            flash("Informe uma distância válida", "error")
            return redirect(url_for("novo_treino"))

        if distancia_km <=0:
            flash("A distância precisa ser maior que zero", "error")
            return redirect(url_for("novo_treino"))

        criar_treino(usuario_id, data_treino, tipo, distancia_km, tempo_segundos, observacao)
        flash("Treino registrado com sucesso", "success")
        return redirect(url_for("historico"))


    return render_template("novo_treino.html")

@app.route("/excluir-treino/<int:treino_id>", methods=["POST"])
def excluir_treino(treino_id):
    if "usuario_id" not in session:
        flash("Faça login para acessar essa página","warning")
        return redirect(url_for("login"))

    usuario_id = session["usuario_id"]
    excluir_treino_bd(treino_id, usuario_id)
    flash("Treino excluido com sucesso", "success")
    return redirect(url_for("historico"))

@app.route('/editar-treino/<int:treino_id>', methods=["GET", "POST"])
def editar_treino(treino_id):
    if "usuario_id" not in session:
        flash("Faça login para acessar essa página","warning")
        return redirect(url_for('login'))

    usuario_id = session["usuario_id"]
    treino = buscar_treino_por_id(treino_id, usuario_id)
    if not treino: 
        flash('Treino não encontrado', "error")
        return redirect(url_for('historico'))

    if request.method == "POST":
        data_treino = request.form['data_treino']
        tipo = request.form['tipo']
        distancia_km = request.form['distancia_km']
        tempo = request.form['tempo']
        observacao = request.form['observacao']

        if not data_treino:
            flash("Informe a data do treino", "error")
            return redirect(url_for("editar_treino", treino_id=treino_id))

        if tipo not in ["corrida", "caminhada"]:
            flash("tipo de treino inválido", "error")
            return redirect(url_for("editar_treino", treino_id=treino_id))

        try: 
            distancia_km = float(distancia_km.replace(",", "."))
        except ValueError:
            flash('Digite uma distância válida', "error")
            return redirect(url_for("editar_treino", treino_id=treino_id))

        try:
            tempo_segundos = transformar_tempo_em_segundos(tempo)
        except ValueError as erro:
            flash(str(erro), "error")
            return redirect(url_for("editar_treino", treino_id=treino_id))

        if distancia_km <= 0:
            flash('Digite uma distância maior que 0', "error")        
            return redirect(url_for("editar_treino", treino_id=treino_id))

        atualizar_treino(treino_id, usuario_id, data_treino, tipo, distancia_km, tempo_segundos, observacao)
        flash('Treino atualizado com sucesso', "success")
        return redirect(url_for("historico"))
    return render_template("editar_treino.html",treino = treino, formatar_tempo=formatar_tempo, formatar_distancia=formatar_distancia)

@app.route("/historico")
def historico():
    if "usuario_id" not in session:
        flash("Faça login para acessar essa pagina","warning")
        return redirect(url_for("login"))

    usuario_id = session["usuario_id"]
    treinos = listar_treinos_usuario(usuario_id)

    return render_template("historico.html", treinos=treinos, formatar_data=formatar_data, formatar_tempo=formatar_tempo, calcular_pace=calcular_pace, formatar_distancia=formatar_distancia )

@app.route("/logout")
def logout():
    session.clear()
    flash("Logout realizado com sucesso", "success")
    return redirect(url_for("login"))

if __name__ == '__main__':
    app.run(debug=True)



