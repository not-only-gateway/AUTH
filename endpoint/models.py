from app import db
from sqlalchemy.exc import SQLAlchemyError

class Endpoint(db.Model):
    __tablename__ = 'endpoint'

    url = db.Column('url', db.String, primary_key=True)
    require_auth = db.Column('requer_autenticacao', db.Boolean, nullable=False)
    denomination = db.Column('denominacao', db.String, nullable=False, unique=True)
    description = db.Column('descricao', db.String)

    def update(self, data):
        try:
            for key in data.keys():
                setattr(self, key, data.get(key, None))

            db.session.commit()
        except SQLAlchemyError:
            pass

    def __init__(self, data):
        for key in data.keys():
            if hasattr(self, key):
                setattr(self, key, data.get(key, None))
        db.session.add(self)
        db.session.commit()


class Access(db.Model):
    __tablename__ = 'endpoint_privilegio'

    method = db.Column('metodo_http',db.String, nullable=False)
    endpoint = db.Column('endpoint', db.String,
                         db.ForeignKey('endpoint.url', ondelete='CASCADE'), primary_key=True)
    privilege = db.Column('privilegio', db.BigInteger,
                          db.ForeignKey('privilegio.codigo_id', ondelete='CASCADE'), primary_key=True)

    def update(self, data):
        try:
            for key in data.keys():
                setattr(self, key, data.get(key, None))

            db.session.commit()
        except SQLAlchemyError:
            pass

    def __init__(self, data):
        for key in data.keys():
            if hasattr(self, key):
                setattr(self, key, data.get(key, None))
        db.session.add(self)
        db.session.commit()
