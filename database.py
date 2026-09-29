import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def conectar_bd():
    conexao = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT")
    )

    return conexao

def criar_usuario(nome, email, senha_hash):
    conexao = conectar_bd()
    cursor = conexao.cursor()
    cursor.execute(
        "INSERT INTO usuarios (nome, email, senha_hash) "
        "VALUES (%s, %s, %s)",(nome, email, senha_hash)
    )
    conexao.commit()
    cursor.close()
    conexao.close()

def buscar_usuario_por_email(email):
    conexao = conectar_bd()
    cursor = conexao.cursor()
    cursor.execute(
        "SELECT * FROM usuarios WHERE email = %s", (email,)
    )
    usuario = cursor.fetchone()

    cursor.close()
    conexao.close()
    return usuario

def criar_treino(usuario_id, data_treino, tipo, distancia_km, tempo_segundos, observacao):
    conexao = conectar_bd()
    cursor = conexao.cursor()

    cursor.execute(
        """INSERT INTO treinos (usuario_id, data_treino, tipo, distancia_km, tempo_segundos, observacao)
        VALUES(%s,%s,%s,%s,%s,%s)""", (usuario_id, data_treino, tipo, distancia_km, tempo_segundos, observacao)
        
    )
    conexao.commit()
    cursor.close()
    conexao.close()

def listar_treinos_usuario(usuario_id):
    conexao = conectar_bd()
    cursor = conexao.cursor()
    cursor.execute(
        ''' SELECT * FROM treinos WHERE usuario_id = %s
            ORDER BY data_treino DESC''', (usuario_id,)
    )
    treinos = cursor.fetchall()
    cursor.close()
    conexao.close()
    return treinos

def buscar_resumo_treinos_usuario(usuario_id):
    conexao = conectar_bd()
    cursor = conexao.cursor()
    cursor.execute(
        '''
        SELECT COUNT(*), COALESCE(SUM(distancia_km),0), COALESCE(SUM(tempo_segundos),0)
        FROM treinos WHERE usuario_id = %s    
        ''', (usuario_id,)    
    )
    resumo_treinos = cursor.fetchone()
    cursor.close()
    conexao.close()
    return resumo_treinos

def buscar_treino_por_id(treino_id, usuario_id):
    conexao = conectar_bd()
    cursor = conexao.cursor()
    cursor.execute(
        '''
            SELECT * FROM treinos WHERE id = %s
            AND usuario_id = %s
        ''', (treino_id, usuario_id)
    )
    treino = cursor.fetchone()
    cursor.close()
    conexao.close()
    return treino

def excluir_treino(treino_id,usuario_id):
    conexao = conectar_bd()
    cursor = conexao.cursor()
    cursor.execute(
        '''
        DELETE FROM treinos WHERE id = %s 
        AND usuario_id = %s    
        ''',(treino_id,usuario_id)
    )
    conexao.commit()
    cursor.close()
    conexao.close()

def atualizar_treino(treino_id, usuario_id, data_treino, tipo, distancia_km, tempo_segundos, observacao):
    conexao = conectar_bd()
    cursor = conexao.cursor()
    cursor.execute(
        '''
        UPDATE treinos SET data_treino=%s, tipo=%s, distancia_km=%s, tempo_segundos=%s, observacao=%s
        WHERE id=%s AND usuario_id=%s
        ''',(data_treino, tipo, distancia_km, tempo_segundos, observacao, treino_id, usuario_id)
    )
    conexao.commit()
    cursor.close()
    conexao.close()



if __name__ == "__main__":
    treinos = listar_treinos_usuario(6)
    print(treinos)

    





