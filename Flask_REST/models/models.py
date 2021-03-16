from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from marshmallow_sqlalchemy import ModelSchema

from sqlalchemy.dialects.postgresql import JSON

from instance.config import * 

db = SQLAlchemy()

# association table many-to-many relationship between articles and channels
ass_table = db.Table('ass_table',
                     db.Column('article_url', db.String, db.ForeignKey('article_model.article_url')),
                     db.Column('channel', db.Integer, db.ForeignKey('channel_model.channel')),
                     db.Column('time_added', db.DateTime, nullable=False, default=datetime.utcnow))

class ChannelModel(db.Model):
    channel = db.Column(db.String, primary_key=True)
    articles = db.relationship("ArticleModel", secondary=ass_table)

    def __repr__(self):
        return f"channel: {self.channel}\n"

class ArticleModel(db.Model):
    article_url = db.Column(db.String, primary_key=True)
    title = db.Column(db.String, nullable=False)
    word_count = db.Column(db.Integer, nullable=False)
    channels = db.relationship("ChannelModel", secondary=ass_table)

    def __repr__(self):
        return f"url: {self.url}\n title: {self.title}\n wordcount: {self.word_count}\n\n"



# Schemas for marshmallow_sqlalchemy
class ArticleSchema(ModelSchema):
    class Meta:
        model = ArticleModel

class ChannelSchema(ModelSchema):
    class Meta:
        ordered = False
        model = ChannelModel
