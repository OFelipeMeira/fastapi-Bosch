from tortoise.models import Model
from tortoise import fields

class Persons(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    cpf = fields.CharField(max_length=11)
