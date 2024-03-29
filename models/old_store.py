from db import db

class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)    
    name = db.Column(db.String(80))

    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, name):
        self.name = name

    def json(self):
        return {'name': self.name, 'items': [items.json() for item in self.items.all()]}


    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

        if row:
            #return cls(row[0], row[1]}}  # Agora vai retornar um objeto da própria classe ao invez de uma tupla
            return cls(*row)


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delet_from_db(self):
        db.session.delete(self)
        db.session.commit()