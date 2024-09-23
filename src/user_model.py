from flask_login import UserMixin
from utils import db
from sqlalchemy import Sequence, event

custom_id_seq = Sequence('custom_id_seq', start=1, metadata=db.metadata)

class Users(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.String(50), primary_key=True, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    gender = db.Column(db.String(7), nullable=False)
    branch = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(15), nullable=False)


@event.listens_for(Users, 'before_insert')
def generate_custom_id(mapper, connection, target):
    next_id = connection.execute(custom_id_seq.next_value()).scalar()

    target.id = f"anfa{next_id:04d}"