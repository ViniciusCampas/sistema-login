def insertTable(cursor,valor):
    cursor.execute('''
        INSERT INTO USUARIO(
            EMAIL,
            SENHA
            ) VALUES(?,?)
    ''',(valor.email,valor.senha)) 

def updateTable(cursor,valor,loginID):
    cursor.execute('''
        UPDATE USUARIO SET
            EMAIL = ?,
            SENHA = ?
        WHERE ID = ?
    ''',(valor.email,valor.senha,loginID))

def deleteTable(cursor,loginID):
    cursor.execute('DELETE FROM USUARIO WHERE ID = ?',(loginID,))

def selectTable(cursor):
    cursor.execute('SELECT * FROM USUARIO')
    rows= cursor.fetchall()
    return [dict(row) for row in rows]

# Busca usuário pelo email, retorna senha hash caso exista
def selectTableEmail(cursor,email):
    cursor.execute('SELECT * FROM USUARIO WHERE EMAIL = ?',(email,))
    rows= cursor.fetchone()
    if rows:
        user=dict(rows)
        return user['SENHA']
    return False
