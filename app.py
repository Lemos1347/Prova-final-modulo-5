# Importando as bibliotecas necessárias
from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

# Variáveis com as informações necessárias para estabelecer uma conexão com o banco de dados
engine = create_engine("sqlite+pysqlite:///database.db")
base = declarative_base()
Session = sessionmaker(engine)
db = Session()

# Criando um objeto flask para criar rotas e iniciar um servidor
app = Flask(__name__)

# Classe que reprensenta o esquema da minha tabela no meu banco de dados
class Game(base):
    # Nome da tabela
    __tablename__ = "games"
    # Variáveis que representam as colunas e seus respectivos nomes e o que cada uma aceita
    id = Column(Integer, primary_key=True)
    nome = Column(String)
    plataforma = Column(String)
    preco = Column(String)
    quantidade = Column(Integer)

   # Método da classe para facilitar a resposta ao usuário. Posto que quando faço uma querry para retornar o que tenho em meu banco de dados, a resposta que meu programa recebe não é uma variável que posso converter direto para JSON, assim, primeiro crio um dicinário para quando necessário eu consiga responder um JSON na minha rota.
    def to_dict(self):
        return {"id": self.id, "nome": self.nome, "plataforma": self.plataforma, "preco": self.preco, "quantidade": self.quantidade}

# Executando uma função do ORM SQLAlchemy para sicronizar o meu banco de dados com os esquemas das minhas tabelas, caso elas ainda não existam, elas são criadas nesse momento 
base.metadata.create_all(engine)

# Inicio das rotas

# Rota para pegar todos os jogos disponíveis no banco de dados
@app.get('/jogos')
def handle_get_jogos():
    # Executando um try except para evitar que meu programe crache caso aconteça algum erro
    try:
        # Executo uma função na variável que estabelece uma conexão com o banco de dados para extrair todos os dados da tabela 'games'(a classe 'Game' faz uma referência a essa tabela)
        games = db.query(Game).all()
        response = []
        # O que foi retornado para a variável games é um array de objetos, assim, faço um loop para pegar cada objeto e executo a função criadad na classe 'Game' para que eu armazene em um array os dicionários referentes a cada linha da minha tabela em meu banco de dados
        for game in games:
            response.append(game.to_dict())
         # Retorno ao usuário um array de dicionários
        return response
    except Exception as err:
        # Retorno ao usuário um JSON com a mesagem do erro que o programa gerou e o status code 500.
        return jsonify(str(err)), 500

# Rota para criar um jogo no banco de dados
@app.post("/jogo/create")
def handle_create_jogo():
    # Executando um try except para evitar que meu programe crache caso aconteça algum erro
    try:
        # Pego as informações fornecidas pelo usuário através de um json
        data = request.json
        # Crio um objeto 'game' advindo da classe Game, a qual representa um esquema da minha tabela no meu banco de dados
        game = Game(nome= data['nome'],plataforma=data['plataforma'], preco= data['preco'], quantidade=data['quantidade'])
        # Com a variável de conexão já definida na escopo global, adiciono uma linha nova na minha tabela
        db.add(game)
        # Fixo minhas mudanças
        db.commit()
        # Retorno ao usuário uma mensagem de confirmação pois caso alguns dos passos anteriores gere um erro, ele cairá no except e a mensagem de erro será entregue ao usuário
        return jsonify({'message': 'sucess!'})
    except Exception as err:
        # Caso aconteça algum erro, retorno ao usuário um JSON que conterá a mensagem de erro gerada e um status code 500.
        return jsonify({'message': str(err)}), 500

if '__main__' == __name__:
    # Rodanod meu app com a propriedade debug True para facilitar o desenvolvimento
    app.run(debug=True, host="0.0.0.0", port=3001)