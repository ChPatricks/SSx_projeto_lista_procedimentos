#import pyodbc
import sqlite3
from flask import Flask, render_template, request, jsonify


app = Flask(__name__)

def obter_conexao():
    conexao = sqlite3.connect("banco/clientes.db")
    return conexao

    """"    driver = '{SQL Server}'
    server = 'PATRICK-NOTE\\SQLEXPRESS'
    data_base = 'SSx'
    user = 'PATRICK-NOTE\\PATRICK'

    conexao = sqlite3.connect(
        f'DRIVER={driver};'
        f'SERVER={server};'
        f'DATABASE={data_base};'
        f'UID='';'
        f'PWD='';')
        """
    
def criar_tabela_e_inserir_clientes():
    conn = obter_conexao()
    #conn = sqlite3.connect("banco/clientes.db")
    cursor = conn.cursor()

    # Cria a tabela se não existir
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        idade INTEGER,
        ativo INTEGER
    )
    """)

    # Dados de exemplo
    clientes = [
        ("Ana Souza", 28, 1),
        ("Carlos Lima", 35, 0),
        ("Marina Alves", 22, 1),
        ("João Pedro", 41, 1),
        ("Beatriz Moura", 30, 0),
        ("Lucas Rocha", 27, 1),
        ("Fernanda Dias", 33, 1),
        ("Ricardo Nunes", 29, 0),
        ("Juliana Costa", 26, 1),
        ("Paulo Mendes", 38, 1)
    ]

    # Insere os clientes
    cursor.executemany(
        "INSERT INTO clientes (nome, idade, ativo) VALUES (?, ?, ?)",
        clientes
    )

    conn.commit()
    conn.close()

    print('tabela criada e clientes inseridos')

def obter_clientes():
    conn = obter_conexao()
    cursor = conn.cursor()
    query = "SELECT ID, NOME, IDADE, ATIVO FROM clientes"
    cursor.execute(query)
    clientes = cursor.fetchall()
    conn.close()

    return clientes

def filtrar_cliente(termo=''):
    print(termo)
    conn = obter_conexao()
    cursor = conn.cursor()
    query = """SELECT ID, NOME, IDADE, ATIVO
            FROM clientes
            WHERE    NOME          LIKE ?
            OR CAST (ID    AS TEXT) LIKE ?
            OR CAST (IDADE AS TEXT) LIKE ?
            OR CAST (ATIVO AS TEXT) LIKE ?  """
    
    cursor.execute(query, (f'%{termo}%', f'%{termo}%', f'%{termo}%', f'%{termo}%'))
    cliente_filtrado = cursor.fetchall()
    clientes = [list(row) for row in cliente_filtrado]  # converte tuplas para listas (JSON serializável)
    conn.close()

    return clientes

def obter_procedimentos():
    conn = obter_conexao()
    cursor = conn.cursor()
    cursor.execute("SELECT ID, PROCEDIMENTO, ATIVO FROM teste_procedimentos")
    procedimentos = cursor.fetchall()

    return procedimentos
    
# Rota principal (exibe o HTML index.html)
@app.route('/')
def index():
    criar_tabela_e_inserir_clientes()
    clientes = obter_clientes()
    #procedimentos = obter_procedimentos()

    #procedimentos_apurado = []
    #for procedimento in procedimentos:
    #    if procedimento[2]:
    #        procedimentos_apurado.append(procedimento)

    dados = {
        'clientes':clientes,}
        #'procedimentos': procedimentos_apurado
    #}

    print(dados)

    return render_template('index.html', **dados)

# Rota chamada via JavaScript (AJAX)
@app.route('/filtro_clientes')
def filtrar():
    termo = request.args.get('termo', '')  # recebe o termo da URL
    clientes_filtrados = filtrar_cliente(termo)
    return jsonify(clientes_filtrados)  # retorna JSON para o JS

if __name__ == '__main__':
    #criar_tabela_e_inserir_clientes()
    app.run(debug=True)