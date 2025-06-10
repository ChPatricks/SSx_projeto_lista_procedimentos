import pyodbc
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/testar-conexao', methods=['GET'])
def obter_conexao():  
    #Meu PC
    driver = '{SQL Server}'
    server = 'PATRICK-NOTE\\SQLEXPRESS'
    data_base = 'SSx'
    user = 'PATRICK-NOTE\\PATRICK'
    senha = ''

    #SSx
    #driver = '{SQL Server}'
    #server = '191.8.144.226,12050'
    #data_base = 'Doctor'
    #user = 'sa'
    #senha = '11'

    conexao = pyodbc.connect(
        f'DRIVER={driver};'
        f'SERVER={server};'
        f'DATABASE={data_base};'
        'Trusted_Connection=yes;') #--> remover isso se for entrar pelo banco externo SSx
        #f'UID={user};'  --> adicionar se for entrar pelo banco externo ssx
        #f'PWD={senha};')--> adicionar se for entrar pelo banco externo ssx

    print('BANCO.PY -> CONECTADO')
    
    return conexao
    
@app.route('/api/carregar_clientes', methods=['GET'])
def obter_clientes():
    conn = obter_conexao()
    cursor = conn.cursor()
    query = "SELECT ID, NOME, IDADE, ATIVO FROM clientes"
    cursor.execute(query)

    colunas = [col[0] for col in cursor.description]  # ['id', 'nome', 'idade', 'ativo']
    clientes = [dict(zip(colunas, linha)) for linha in cursor.fetchall()]

    conn.close()

    #print(f'----->{clientes}')
    return jsonify(clientes)

def filtrar_cliente(termo=''):
    try:
        conn = obter_conexao()
        cursor = conn.cursor()
        query = """SELECT ID, NOME, IDADE, ATIVO
                FROM clientes
                WHERE    NOME          LIKE ?
                OR CAST (ID    AS VARCHAR (150)) LIKE ?
                OR CAST (IDADE AS VARCHAR (150)) LIKE ?
                OR CAST (ATIVO AS VARCHAR (150)) LIKE ?  """
        
        cursor.execute(query, f'%{termo}%', f'%{termo}%', f'%{termo}%', f'%{termo}%')
        cliente_filtrado = cursor.fetchall()
        clientes = [list(row) for row in cliente_filtrado]  # converte tuplas para listas (JSON serializável)
        conn.close()

        return clientes,200
    
    except Exception as e:
        print("Erro ao buscar cliente:", e)
        return {'mensagem': 'Erro na busca de cliente'}, 500


def obter_procedimentos():
    conn = obter_conexao()
    cursor = conn.cursor()
    cursor.execute("SELECT ID, PROCEDIMENTO, ATIVO FROM TESTE_PROCEDIMENTOS")
    procedimentos = cursor.fetchall()

    return procedimentos
    
# Rota principal (exibe o HTML index.html)
@app.route('/')
def index():  
#    clientes = obter_clientes()
#    procedimentos = obter_procedimentos()
#
#    procedimentos_apurado = []
#    for procedimento in procedimentos:
#        if procedimento[2]:
#            procedimentos_apurado.append(procedimento)
#
#    dados = {
#        'clientes':clientes,
#        'procedimentos': procedimentos_apurado
#    }

    return render_template('index.html')#, **dados)

# Rota chamada via JavaScript (AJAX)
#@app.route('/filtro_clientes')
#def filtrar():
#    termo = request.args.get('termo', '')  # recebe o termo da URL
#    clientes_filtrados = filtrar_cliente(termo)
#    return jsonify(clientes_filtrados)  # retorna JSON para o JS

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)