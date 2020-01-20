from flask_restful import Resource
from models.store import StoreModel

class Store(Resource):
    def get(self, name):
        strore = StoreModel.find_by_name(name)
        if store:
            return store.json()
        return {"message": "Store não encontrada"}, 404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {"message": "A strore com nome '{}' já existe.".format(name)}, 400

        store = StoreModel(name)
        try:
            store.save_to_db()
        except:
            return {"message": "Ocorreu um erro ao tentar salvar a store."}, 500

        return store.json(), 201

    def delete(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {"message": "Store deletada"}


class StoreList(Resource):
    def get(self):
        return {'stores': [x.json() for x in StoreModel.query.all()]}