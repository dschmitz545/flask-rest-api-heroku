import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel

class UserRegister(Resource):

    # Analisador de solitações - Torna os campos obrigatórios na requisição e verifica se os dados
    # entregues estão corretos
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help="O campo usuário é obrigátorio")
    parser.add_argument('password', type=str, required=True, help="O campo password é obrigátorio")

    def post(self):
        # passando os dados obtidos para a variavel
        data = UserRegister.parser.parse_args()

        # Verificando se o usuário informado já está cadastrado
        if UserModel.find_by_username(data['username']): # is not None -  Se isso não for nenhum
            return {"message:": "O usuário informado já existe"}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"message": "user created sucefully."}, 201