from marshmallow_jsonapi import Schema, fields
from marshmallow import validate

from app.users.models import UsersSchema
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.exc import SQLAlchemyError

db = SQLAlchemy()


class CRUD():

    def add(self, resource):
        db.session.add(resource)
        return db.session.commit()

    def update(self):
        return db.session.commit()

    def delete(self, resource):
        db.session.delete(resource)
        return db.session.commit()


class Tasks(db.Model, CRUD):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    description = db.Column(db.String(250), nullable=True)
    due_datetime = db.Column(db.DateTime, server_default=db.func.current_timestamp(), nullable=True)
    # TODO: Find a nice way to create and migrate enums!
    complexity = db.Column(db.Integer)
    urgency = db.Column(db.Integer)
    importance = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    creation_time = db.Column(db.DateTime, server_default=db.func.current_timestamp(), nullable=False)
    is_done = db.Column(db.Boolean, server_default="false", nullable=False)

    def __init__(self, title, complexity, urgency, importance):

        self.title = title
        self.complexity = complexity
        self.urgency = urgency
        self.importance = importance


class TasksSchema(Schema):

    not_blank = validate.Length(min=1, error='Field cannot be blank')
    id = fields.Integer(dump_only=True)
    user_id = fields.Nested(UsersSchema, only=['id', 'name'])
    title = fields.Email(validate=not_blank)


     #self links
    def get_top_level_links(self, data, many):
        if many:
            self_link = "/tasks/"
        else:
            self_link = "/tasks/{}".format(data['id'])
        return {'self': self_link}


    class Meta:
        type_ = 'tasks'
