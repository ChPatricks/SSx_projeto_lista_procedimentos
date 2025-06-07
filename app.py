import pyodbc
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def obter_conexao():
    driver = '{SQL Server}'
    server = 'PATRICK-NOTE\\SQLEXPRESS'
    data_base = 'SSx'
    user = 'PATRICK-NOTE\\PATRICK'
    
    conexao = pyodbc.connect(
        f'DRIVER={driver};'
        f'SERVER={server};'
        f'DATABASE={data_base};'
        f'UID='';'
        f'PWD='';')

    return conexao

def obter_clientes():
    conn = obter_conexao()
    cursor = conn.cursor()
    query = "SELECT ID, NOME, IDADE, ATIVO FROM teste_assinaturas"
    cursor.execute(query)
    clientes = cursor.fetchall()
    conn.close()

    return clientes

def filtrar_cliente(termo=''):
    conn = obter_conexao()
    cursor = conn.cursor()
    query = """SELECT ID, NOME, IDADE, ATIVO
            FROM teste_assinaturas
            WHERE    NOME           LIKE ?
            OR CAST (ID    AS VARCHAR(20)) LIKE ?
            OR CAST (IDADE AS VARCHAR(150)) LIKE ?
            OR CAST (ATIVO AS VARCHAR(1)) LIKE ?  """
    
    cursor.execute(query, f'%{termo}%', f'%{termo}%', f'%{termo}%', f'%{termo}%')
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
    clientes = obter_clientes()
    procedimentos = obter_procedimentos()

    procedimentos_apurado = []
    for procedimento in procedimentos:
        if procedimento[2]:
            procedimentos_apurado.append(procedimento)

    dados = {
        'clientes':clientes,
        'procedimentos': procedimentos_apurado
    }

    print(dados)

    return render_template('index.html', **dados)

# Rota chamada via JavaScript (AJAX)
@app.route('/filtro_clientes')
def filtrar():
    termo = request.args.get('termo', '')  # recebe o termo da URL
    clientes_filtrados = filtrar_cliente(termo)
    return jsonify(clientes_filtrados)  # retorna JSON para o JS

if __name__ == '__main__':
    app.run(debug=True)