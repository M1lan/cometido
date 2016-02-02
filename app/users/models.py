from marshmallow_jsonapi import Schema, fields
from marshmallow import validate
from app.basemodels import db, CRUD


class Users(db.Model, CRUD):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    name = db.Column(db.String(250), nullable=False)
    is_active = db.Column(db.Boolean, server_default="false", nullable=False)
    created_at = db.Column(
        db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
    modified_at = db.Column(
        db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)

    def __init__(self, email, password, name, is_active):

        self.email = email
        self.password = password
        self.name = name
        self.is_active = is_active


class UsersSchema(Schema):

    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    email = fields.Email(validate=not_blank)
    password = fields.Email(validate=not_blank)
    name = fields.String(validate=not_blank)
    is_active = fields.Boolean()
    creation_time = fields.DateTime(dump_only=True)
    modification_time = fields.DateTime(dump_only=True)


     #self links
    def get_top_level_links(self, data, many):
        if many:
            self_link = "/users/"
        else:
            self_link = "/users/{}".format(data['id'])
        return {'self': self_link}


    class Meta:
        type_ = 'users'
