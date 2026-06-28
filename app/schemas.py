from marshmallow import Schema, ValidationError, fields, post_load, validates

from models import Category, Good


class GoodSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)
    category_id = fields.Int(required=True)

    @validates('name')
    def validate_name(self, value, **kwargs):
        if len(value.strip()) < 2:
            raise ValidationError('Name must be at least 2 characters long')

    @validates('price')
    def validate_price(self, value, **kwargs):
        if value < 0:
            raise ValidationError('Price must be greater than or equal to 0')

    @validates('category_id')
    def validate_category_id(self, value, **kwargs):
        if value <= 0:
            raise ValidationError('Category id must be greater than 0')

    @post_load
    def make_good(self, data, **kwargs):
        return Good(**data)


class CategorySchema(Schema):
    category_id = fields.Int(dump_only=True)
    name = fields.Str(required=True)

    @validates('name')
    def validate_name(self, value, **kwargs):
        if len(value.strip()) < 2:
            raise ValidationError('Name must be at least 2 characters long')

    @post_load
    def make_category(self, data, **kwargs):
        return Category(**data)
