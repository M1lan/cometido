import datetime

from marshmallow_jsonapi import Schema, fields
from marshmallow import validate

from app.users.models import UsersSchema
from app.basemodels import db, CRUD


class Tasks(db.Model, CRUD):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(250), nullable=True)
    due_datetime = db.Column(db.DateTime, server_default=db.func.current_timestamp(), nullable=True)
    # TODO: Find a nice way to create and migrate enums!
    complexity = db.Column(db.Integer, nullable=False)
    urgency = db.Column(db.Integer, nullable=False)
    importance = db.Column(db.Integer, nullable=False)
    creation_time = db.Column(db.DateTime, server_default=db.func.current_timestamp(), nullable=False)
    is_done = db.Column(db.Boolean, server_default="false", nullable=False)

    # foreign key - many tasks to one user
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    user_relation = db.relationship('Users', backref="users")

    def __init__(
        self, title, description, due_datetime, complexity, urgency, importance,
        user_id):

        self.title = title
        self.description = description
        self.due_datetime = due_datetime
        self.complexity = complexity
        self.urgency = urgency
        self.importance = importance
        self.created_at = datetime.datetime.now()
        self.user_id = user_id


class TasksSchema(Schema):

    not_blank = validate.Length(min=3, error='Field cannot be blank or so short')

    id = fields.Integer(dump_only=True)
    title = fields.Email(validate=not_blank)
    description = fields.String()
    due_datetime = fields.DateTime(dump_only=True)
    complexity = fields.Integer()
    urgency = fields.Integer()
    importance = fields.Integer()
    created_at = fields.DateTime(dump_only=True)
    is_done = fields.Boolean()
    user_id = fields.Integer()


     #self links
    def get_top_level_links(self, data, many):
        if many:
            self_link = "/tasks/"
        else:
            self_link = "/tasks/{}".format(data['id'])
        return {'self': self_link}


    class Meta:
        type_ = 'tasks'
