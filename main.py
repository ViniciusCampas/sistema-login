from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
import bcrypt
import banco
#Foi instalado o Uvicorn para rodar o servidor na porta http://localhost:8000
#python -m uvicorn main:app --reload

#Nome do arquivo do banco SQLite
DATABASE='dbaLogin.db'

# Cria conexão com o banco de dados, sqlite3.Row permite acessar colunas pelo nome
def getConnection():
    connec= sqlite3.connect(DATABASE)
    connec.row_factory=sqlite3.Row
    return connec

# Cria tabela de usuários caso ela não exista
def createTable():
    connec=getConnection()
    cursor=connec.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS USUARIO(
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            EMAIL TEXT UNIQUE NOT NULL,
            SENHA TEXT NOT NULL)
    ''')
    connec.commit()
    connec.close()


createTable()

class Login(BaseModel):
    email:str
    senha:str

app=FastAPI()

# Cria novo usuário, a senha é convertida para hash antes de salvar
@app.post('/users')
def createUser(login:Login):
    senhaHash= bcrypt.hashpw(login.senha.encode('utf-8'),bcrypt.gensalt())# Gera hash seguro da senha
    login.senha= senhaHash.decode('utf-8')
    connec=getConnection()
    cursor=connec.cursor()
    banco.insertTable(cursor,login)
    connec.commit()
    connec.close()
    return {'message':'Usuário criado'}

# Realiza autenticação do usuário, compara senha digitada com hash salvo no banco
@app.post('/login')
def readUser(login:Login):

    connec=getConnection()
    cursor=connec.cursor()
    user=banco.selectTableEmail(cursor,login.email)
    connec.close()

    validar=False

    if not user:
        return {'message': 'Email ou senha invalidos','login': False}
    validar=bcrypt.checkpw(login.senha.encode('utf-8'),user.encode('utf-8'))

    if validar:
        return {'message': 'Login realizado','login': True}

    return {'message': 'Email ou senha invalidos','login': False}

@app.put('/users/{login_id}')
def updateUser(login_id:int,login:Login):
    senhaHash= bcrypt.hashpw(login.senha.encode('utf-8'),bcrypt.gensalt())
    login.senha= senhaHash.decode('utf-8')
    connec=getConnection()
    cursor=connec.cursor()
    banco.updateTable(cursor,login,login_id)
    connec.commit()
    connec.close()
    return {'message':'Usuário alterado'}

@app.delete('/users/{login_id}')
def deleteUser(login_id:int,login:Login):
    connec=getConnection()
    cursor = connec.cursor()

    user=banco.selectTableEmail(cursor,login.email)

    validar=False

    if not user:
        return {'message': 'Email ou senha invalidos','login': False}
    validar=bcrypt.checkpw(login.senha.encode('utf-8'),user.encode('utf-8'))

    if validar:
        banco.deleteTable(cursor,login_id)
        connec.commit()
        connec.close()
        return {'message': 'Login Deletado'}

    connec.commit()
    connec.close()
    return {'message': 'Email ou senha invalidos'}
