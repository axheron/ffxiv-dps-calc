"""Model for tags in the database"""
from xivdpscalc import db

TAG_NAME_MAX_LENGTH = 64
HEX_COLOR_LENGTH = 7 # #0086BF is 7 characters long

class Tag(db.Model):
  __tablename__ = 'tags'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(TAG_NAME_MAX_LENGTH))
  color = db.Column(db.String(HEX_COLOR_LENGTH)) # hex coloring in the UI

class HasTags:
  @db.declared_attr
  def tags(cls):
    tag_association = db.Table(
      f'{cls.__tablename__}_tags',
      cls.metadata,
      db.Column(
        'tag_id',
        db.ForeignKey('tags.id'),
        primary_key=True
      ),
      db.Column(
        f'{cls.__tablename__}_id',
        db.ForeignKey(f'{cls.__tablename__}.id')
      )
    )
    return db.relationship(Tag, secondary=tag_association)
