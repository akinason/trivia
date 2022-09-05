from marshmallow import Schema, fields


class QuestionSchema(Schema):
    question = fields.String()
    answer = fields.String()
    category_id = fields.Integer()
    difficulty = fields.Integer()
