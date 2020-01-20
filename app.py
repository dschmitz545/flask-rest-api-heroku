import os

from flask import Flask
from flask_jwt import JWT
from flask_restful import Api

from resources.item import Item, ItemList
from resources.store import Store, StoreList
from resources.user import UserRegister
from security import authenticate, identity

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'diego'
api = Api(app)

jwt = JWT(app, authenticate, identity) # aqui já vai criar a rota /auth também

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(StoreList, '/stores')

api.add_resource(UserRegister, '/register')

# Significa que so vai executar esse método se esse arquivo for o arquivo principal(main)
# que é definido quando rodamos o programa
# se esse arquivo for usado para ser importado em outro arquivo
# essa verificação baixo não será executado, pois esse arquivo não será o arquivo main do projeto
if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=8000, debug=True)
