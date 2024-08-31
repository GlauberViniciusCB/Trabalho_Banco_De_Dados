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

# Dados para conectar ao banco de dados
conn = pymysql.connect(
  host="localhost",
  user="root",
  password="Minas@0202",
  database="Showdomilhao",
  charset="utf8mb4"
)

#Método para realizar login
@app.route('/', methods=['GET', 'POST'])
def root():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']

        print(email)
        print(senha)

        # Consultar no banco de dados se o jogador está cadastrado
        mycursor = conn.cursor()
        sql = "SELECT * FROM jogador WHERE email = %s"
        val = (email,)
        mycursor.execute(sql, val)
        jogador = mycursor.fetchone()
        print(jogador)

        #Consultar no banco de dados se a senha está correta
        if jogador[3] == senha:
            return redirect(url_for('menu', email=email))
        else:
            return render_template('index.html', error='Usuário ou senha inválidos.')
    else:
        return render_template('index.html')

#Metodo para entrar no menu do jogo
@app.route('/menu/<string:email>', methods=['GET', 'POST'])
def menu(email):
    return render_template('menu.html', email=email)

#Método para um jogador se cadastrar
@app.route('/cadastro', methods=['POST','GET'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        confirmasenha = request.form['confirmasenha']
        print(request.form)

        if senha == confirmasenha:
            # Inserir dados no banco de dados
            mycursor = conn.cursor()
            sql = "INSERT INTO jogador (nome, email, senha) VALUES (%s, %s, %s)"
            val = (nome, email, senha)
            mycursor.execute(sql, val)
            conn.commit()

            return render_template('index.html', sucesso=True)
        else:
            return render_template('cadastro.html', erro='As senhas não coincidem.')
    else:
        return render_template('cadastro.html')

# Inserir uma nova partida no banco de dados, associando ao email
@app.route('/iniciar_partida/<string:email>', methods=['GET'])
def iniciar_partida(email):    
    cursor = conn.cursor()
    sql = "SELECT idjogador FROM jogador WHERE email = %s"
    cursor.execute(sql, (email,))
    idjogador = cursor.fetchone()

    if idjogador:  # Verificar se o jogador foi encontrado e iniciar a partida
        sqlpartida = "INSERT INTO partida (idjogador, pontuacaoparcial, rodada) VALUES (%s, 0, 0)"
        cursor.execute(sqlpartida, (idjogador[0],))
        conn.commit()

        # Obter o ID da partida recém-inserida
        cursor.execute("SELECT LAST_INSERT_ID()")
        id_partida = cursor.fetchone()[0]

        # Redirecionar para a homePage com o ID da partida
        return redirect(url_for('buscar_pergunta', id_partida=id_partida))
    else:
        # Tratar o caso em que o jogador não foi encontrado
        return "Jogador não encontrado"

#Função que começa o jogo
@app.route('/homePage/<int:id_partida>', methods=['GET', 'POST'])
def buscar_pergunta(id_partida):
    mycursor = conn.cursor()
    rodada_atual = None 

    # Verificar se a partida já atingiu o número máximo de rodadas, indicando que o jogador ganhou
    sql = "SELECT rodada FROM partida WHERE idpartida = %s"
    mycursor.execute(sql, (id_partida,))
    resultado = mycursor.fetchone()
    rodada_atual = resultado[0] if resultado else 0
    if rodada_atual == 10:
        print("Você se tornou um milionário")
        return render_template('vitoria.html')
    
    #Verificar se o jogador quis parar no marco 5 ou 9
    
    if request.method == 'POST':
        if rodada_atual in (5, 9):
            if 'acao' in request.form and request.form['acao'] == 'parar':            
                print(f"Parou na rodada {rodada_atual}")

                # Atualizar o banco de dados
                sql = "UPDATE partida SET rodada = %s WHERE idpartida = %s"
                mycursor.execute(sql, (rodada_atual, id_partida))
                conn.commit()
                return render_template('desistiu.html')

        else:
            print(f"Não parou ainda")

 # Buscar uma pergunta aleatória no banco de dados, dentre as 100 perguntas cadastradas   
    mycursor.execute("SELECT * FROM pergunta ORDER BY RAND() LIMIT 1")
    perguntaatual = mycursor.fetchone()
    idpergunta = perguntaatual[0]
    
#Seleção no BD das alternativas relacionadas ao idpergunta da pergunta atual
    sql = (f"SELECT idalternativa, conteudo, alternativacorreta FROM alternativa WHERE idpergunta = {idpergunta}")
    val = (idpergunta)
    mycursor.execute(sql)
    alternativas = mycursor.fetchall() #busca todas as alternativas relacionadas ao idpergunta
    
    #Este laço For converte uma lista de tuplas (onde cada tupla representa uma alternativa que está salva no BD, com um número 
    # e um texto) em uma lista de dicionários, onde cada dicionário representa uma alternativa para ficar mais fácil de manipular.
    aux = 1     
    lista_alternativas = []
    for alt in alternativas:
        dict_alternativas = {"numero": aux, "texto": alt[1], "alternativacorreta": alt[2], "id": alt[0]}
        lista_alternativas.append(dict_alternativas)         
        aux = aux +1  
    
    #Esta estrutura condicional verifica se a resposta está correta
    if request.method=="POST":
        resposta_usuario = request.form['resposta']
        sql = "SELECT alternativacorreta FROM alternativa WHERE idalternativa = %s"
        val = (resposta_usuario)
        mycursor.execute(sql, val)
        resultado = mycursor.fetchone()
        print(resultado)
        if resultado[0] == 1:
            print("Resposta correta")
            
            #Os comandos abaixo atualizam a rodada e a pontuação atual do jogador
            sqlpontuacao = "UPDATE partida SET pontuacaoparcial = pontuacaoparcial + 100000 WHERE idpartida = %s"           
            mycursor.execute(sqlpontuacao, (id_partida,))
            conn.commit()
            sqlrodada = "UPDATE partida SET rodada = rodada + 1 WHERE idpartida = %s"
            mycursor.execute(sqlrodada, (id_partida,))
            conn.commit()
        else: 
            print("Resposta errada.")   
            return render_template('derrota.html')         

    #Prints para testar antes de enviar para o front end
    print (idpergunta)
    print (perguntaatual)
    print (alternativas)

    # Envia os dados para o template
    return render_template('homePage.html', id_partida=id_partida, pergunta=perguntaatual, alternativas=lista_alternativas, rodada_atual=rodada_atual)

#Metodo para troca de senhas (esqueci a senha)
@app.route('/esqueceusenha', methods=['GET', 'POST'])
def trocar_senha():
    if request.method == 'POST':
        email = request.form['email']
        nova_senha = request.form['nova_senha']
        confirmar_senha = request.form['confirmar_senha']
        print(email)
       
        # Consultar no banco de dados se o email é válido
        mycursor = conn.cursor()
        sql = "SELECT * FROM jogador WHERE email = %s"
        val = (email,)
        mycursor.execute(sql, val)
        jogador = mycursor.fetchone()

        #Atualizar a senha no banco de dados
        if jogador:
            if nova_senha == confirmar_senha:
                sql = "UPDATE jogador SET senha = %s WHERE email = %s"
                val = (confirmar_senha, email)
                mycursor.execute(sql, val)
                conn.commit()
                print("Senha alterada com sucesso.")            
        else:
            return render_template('index.html', error='Usuário inválido.')
    else:
        return render_template('index.html')


if __name__ == '__main__':
    #Debug = true para ver os erros mais detalhados
    app.run(debug=True)