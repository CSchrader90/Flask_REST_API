from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from marshmallow_sqlalchemy import ModelSchema
import uuid

from sqlalchemy.dialects.postgresql import JSON

from instance.config import * 

db = SQLAlchemy()

class UserModel(db.Model):
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String(200))
    private_id  = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    is_root  = db.Column(db.Boolean)

# association table many-to-many relationship between articles and channels
ass_table = db.Table('ass_table',
                     db.Column('article_id', db.Integer, db.ForeignKey('article_model.article_id')),
                     db.Column('channel', db.String, db.ForeignKey('channel_model.channel')),
                     db.Column('time_added', db.DateTime, nullable=False, default=datetime.utcnow))

class ChannelModel(db.Model):
    user    = db.Column(db.String, db.ForeignKey('user_model.username'))
    channel = db.Column(db.String, primary_key=True)
    articles = db.relationship("ArticleModel", secondary=ass_table)

    def __repr__(self):
        return f"channel: {self.channel}\n"

class ArticleModel(db.Model):
    user    = db.Column(db.String, db.ForeignKey('user_model.username'))
    article_id = db.Column(db.Integer, primary_key=True)
    article_url = db.Column(db.String)
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
