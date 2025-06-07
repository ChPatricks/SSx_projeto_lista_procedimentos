from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Configuração do banco de dados SQLite para exemplo local
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'dados.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelos
class Procedimento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    valor = db.Column(db.Float, nullable=False)
    imagem_id = db.Column(db.Integer, db.ForeignKey('imagem.id'))

class Imagem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    caminho = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.String(255))
    procedimento = db.relationship('Procedimento', backref='imagem', lazy=True)

# Rotas
@app.route('/')
def index():
    procedimentos = Procedimento.query.all()
    return render_template('index.html', procedimentos=procedimentos)

@app.route('/novo', methods=['GET', 'POST'])
def novo():
    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        valor = float(request.form['valor'])
        imagem_path = request.form['imagem']

        nova_imagem = Imagem(caminho=imagem_path, descricao='Imagem principal')
        db.session.add(nova_imagem)
        db.session.commit()

        novo_proc = Procedimento(nome=nome, descricao=descricao, valor=valor, imagem_id=nova_imagem.id)
        db.session.add(novo_proc)
        db.session.commit()

        return redirect(url_for('index'))

    return render_template('novo.html')

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)