from flask_jwt import jwt_required
from flask_restful import Resource, reqparse

from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()       # cerifica que so pode aceitar campos especificos
    parser.add_argument('price',
        type=float,
        required=True,
        help="Esse valor não pode ficar em branco!"
    )

    parser.add_argument('store_id',
        type=int,
        required=True,
        help="Todo item precisa de uma loja"
    )

    @jwt_required()
    def get(self, name):        # get = read
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item não encontrado'}, 404
    
    
    def post(self, name):                               # post = create
        if ItemModel.find_by_name(name): # poderia ser Item.find_by_name(name):
            return {'message': "o item com o nome '{}' já existe.".format(name)}, 400

        data = Item.parser.parse_args()

        #item = ItemModel(name, data['price'], data['store_id'])
        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {"message": "Ocorreu um erro ao inserir o item."}, 500

        return item.json(), 201
    
    def delete(self, name):                                 # delete = delete
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': 'Item deletado'}

    @jwt_required()
    def put(self, name):        # update = put
        
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)
        
        if item is None:
           #item = ItemModel(name, data['price'], data['store_id'])                    # adiciona - insert
           item = ItemModel(name, **data)
        else:
            item.price = data['price']

        item.save_to_db()

        return item.json()

class ItemList(Resource):
    
    @jwt_required()
    def get(self):
        #return {'items': [item.json() for item in ItemModel.query.all()]}
        #return {'items': list(map(lambda x: x.json(),ItemModel.query.all()))}
        return {'items': [x.json() for x in ItemModel.query.all()]}
