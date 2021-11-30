from marshmallow import Schema, fields, validate, post_load

from models import User, Student, Rating


class UserSchema(Schema):
    id = fields.Integer()
    name = fields.Str(validate=validate.Length(max=45), nullable=False)
    surname = fields.Str(validate=validate.Length(max=45), nullable=False)
    username = fields.Str(validate=validate.Length(max=45), nullable=False)
    password = fields.Str(validate=validate.Length(max=1000), required=True)
    accessusers = fields.Str(validate=validate.OneOf(["Admin", "User"]), required=True)

    @post_load
    def make_user(self, data, **kwargs):
        return User(**data)


class StudentSchema(Schema):
    id = fields.Integer()
    firstname = fields.Str(validate=validate.Length(max=45), required=True)
    surname = fields.Str(validate=validate.Length(max=45), required=True)
    course = fields.Integer(required=True)
    best_grade = fields.Integer(required=True)
    created = fields.Integer(required=True)

    @post_load
    def make_student(self, data, **kwargs):
        return Student(**data)


class RatingSchema(Schema):
    id = fields.Integer()
    title = fields.Str(validate=validate.Length(max=45), required=True)
    Student_id = fields.Integer(required=True)
    user_creator_id = fields.Integer(required=True)

    @post_load
    def make_rating(self, data, **kwargs):
        return Rating(**data)
