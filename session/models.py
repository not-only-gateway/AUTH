from app import db
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.exc import SQLAlchemyError

class Session(db.Model):
    __tablename__ = 'sessao'

    id = db.Column('codigo_id', db.BigInteger, primary_key=True)
    user = db.Column('usuario', db.String, db.ForeignKey('usuario.email_usuario', ondelete='CASCADE'), nullable=False)
    max_life = db.Column('vida_maxima_token', db.DateTime, nullable=False)
    creation_time = db.Column('data_criacao', db.DateTime, nullable=False)
    ip_address = db.Column('endereco_ip', db.String, nullable=False)


    token_uuid = db.Column('token_uuid', UUID(as_uuid=True), nullable=False)
    ad = db.Column('ad', db.BigInteger, db.ForeignKey('ad.codigo_id', ondelete='CASCADE'), nullable=False)

    def __init__(self, data):
        try:
            for key in data.keys():
                setattr(self, key, data.get(key, None))
            db.session.add(self)
            db.session.commit()
        except SQLAlchemyError:
            pass
