from flask import Flask, render_template, request, redirect, url_for
import pymysql
import sqlalchemy
import pandas as pd
from sqlalchemy import create_engine

app = Flask(__name__, static_url_path='/static')

# Configuração do banco de dados via wsl
# mydb = pymysql.connect(
#   host="172.19.64.1",
#   user="wsl_user",
#   password="12345",
#   database="Showdomilhao"
# )

mydb = pymysql.connect(
  host="localhost",
  user="root",
  password="Minas@0202",
  database="Showdomilhao"
)

# engine = create_engine('mysql://root:Minas@0202@host/showdomilhao')
# df = pd.read_csv('meu_arquivo.csv')
# df.to_sql('nome_da_tabela', con=engine, if_exists='append', index=False)

# Realizar login
@app.route('/', methods=['GET', 'POST'])
def root():
    return render_template('index.html')
# def indexlogin():
#     if request.method == 'POST':
#         email = request.form['email']
#         senha = request.form['senha']

#         # Consultar o banco de dados
#         mycursor = mydb.cursor()
#         sql = "SELECT * FROM jogador WHERE email = %s"
#         val = (email,)
#         mycursor.execute(sql, val)
#         jogador = mycursor.fetchone()

#         if jogador and jogador[3] == senha:
#              return redirect(url_for('menu'))  # Redireciona para a página inicial onde o jogador escolhe se quer jogar
#                                               # ou ver as estatíticas
#         else:
#             return render_template('index.html', error='Usuário ou senha inválidos.')

#     PATH = '../assets/Html/index.html'
#     return render_template(PATH)


# Rota para salvar dados do formulário
@app.route('/cadastro', methods=['GET'])
def cadastrar():
  return render_template('cadastro.html')

# Rota para salvar dados do formulário
@app.route('/salvar', methods=['POST'])
def salvar():
  nome = request.form['nome']
  email = request.form['email']
  senha = request.form['senha']

 # Inserir dados no banco de dados
  mycursor = mydb.cursor()
  sql = "INSERT INTO jogador (nome, email, senha) VALUES (%s, %s, %s)"
  val = (nome, email, senha)
  mycursor.execute(sql, val)
  mydb.commit()

  return "Cadastro bem sucedido!"

app.run()





