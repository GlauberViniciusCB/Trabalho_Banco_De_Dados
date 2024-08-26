from flask import Flask, render_template, request, redirect, url_for
import pymysql
import sqlalchemy
import pandas as pd
import csv
from sqlalchemy import create_engine
import chardet

app = Flask(__name__, static_url_path='/static')

# Configuração do banco de dados via wsl
# conn = pymysql.connect(
#   host="172.19.64.1",
#   user="wsl_user",
#   password="12345",
#   database="Showdomilhao"
# )

# Conectar ao banco de dados
conn = pymysql.connect(
  host="localhost",
  user="root",
  password="Minas@0202",
  database="Showdomilhao",
  charset="utf8mb4"
)

"""engine = create_engine('mysql://root:Minas@0202@host/showdomilhao')
df = pd.read_csv('pergunta.csv')
df.to_sql('pergunta', con=engine, if_exists='append', index=False)"""

@app.route('/', methods=['GET', 'POST'])
def root():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        # Consultar o banco de dados
        mycursor = conn.cursor()
        sql = "SELECT * FROM jogador WHERE email = %s"
        val = (email,)
        mycursor.execute(sql, val)
        jogador = mycursor.fetchone()

        if jogador and jogador[3] == senha:
            return redirect(url_for('menu'))
        else:
            return render_template('index.html', error='Usuário ou senha inválidos.')
    else:
        return render_template('index.html')


@app.route('/cadastro', methods=['GET'])
def cadastrar():
    return render_template('cadastro.html')

@app.route('/salvar', methods=['POST'])
def salvar():
    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['senha']

    # Inserir dados no banco de dados
    mycursor = conn.cursor()
    sql = "INSERT INTO jogador (nome, email, senha) VALUES (%s, %s, %s)"
    val = (nome, email, senha)
    mycursor.execute(sql, val)
    conn.commit()

    return render_template('index.html')

# Função para buscar uma pergunta aleatória
@app.route('/homePage', methods=['GET', 'POST'])
def buscar_pergunta():
    mycursor = conn.cursor()
    mycursor.execute("SELECT * FROM pergunta ORDER BY RAND() LIMIT 1")
    perguntaatual = mycursor.fetchone()
    idpergunta = perguntaatual[0]

    sql = (f"SELECT conteudo FROM alternativa WHERE idpergunta = {idpergunta}")
    val = (idpergunta)
    mycursor.execute(sql)
    alternativas = mycursor.fetchall()
    
    aux = 1
    lista_alternativas = []
    for alt in alternativas:
        dict_alternativas = {"numero": aux, "texto": alt[0]}
        lista_alternativas.append(dict_alternativas)         
        
        aux = aux +1
    
    print (idpergunta)
    print (perguntaatual)
    print (alternativas)
    # Passando os dados para o template
    return render_template('homePage.html', pergunta=perguntaatual, alternativas=lista_alternativas)

"""@app.route('/', methods=['GET', 'POST'])
def quiz():
    if request.method == 'POST':
        resposta_usuario = request.form['resposta'] == 'True'  # Convertendo a resposta para booleano
        pergunta_atual = session.get('pergunta_atual')
        if resposta_usuario == pergunta_atual[5]:
            return "Resposta correta!"
        else:
            return "Resposta incorreta!"
    else:
        pergunta = buscar_pergunta()
        session['pergunta_atual'] = pergunta
        return render_template('quiz.html', pergunta=pergunta)

if __name__ == '__main__':
    app.secret_key = 'your_secret_key'  # Substitua por uma chave secreta
    app.run(debug=True)"""

if __name__ == '__main__':
    app.run()
    buscar_pergunta()