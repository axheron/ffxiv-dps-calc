"""Model for saving gearsets in the database"""
from xivdpscalc import db


class Gearset(db.Model):
    __tablename__ = 'gearsets'

    id = db.Column(db.Integer, primary_key=True) # TODO: swap to uuid per discussion
    name = db.Column(db.String(64))
    description = db.Column(db.Text())
    etro_id = db.Column(db.String(36)) # TODO: implement uuid type
    stats = db.Column(db.JSON()) # TODO: This basically shoehorns us into postgres
    estimates = db.Column(db.JSON())
    sim_version = db.Column(db.String(9)) # TODO: think about this
    recommended = db.Column(db.Boolean())
