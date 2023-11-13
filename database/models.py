from os import name
from tortoise.models import Model
from tortoise import fields

class Account(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    cpf = fields.CharField(max_length=11)

    def __str__(self):
        return self.name