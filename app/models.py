from . import db
from .utils.json_utils import json_able


@json_able
class Product(db.Model):
    __tablename__ = 'Product'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(40))
    remark = db.Column(db.String(1000), nullable=True)
    isBuy = db.Column(db.Integer, default=1)
