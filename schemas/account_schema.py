"""
    Structures to convert JSON into MODELs, MODELs into JSON
    and verify if there isn't any info missing
"""

from typing import Optional
from pydantic import BaseModel as SchemaBaseModel

class AccountSchema(SchemaBaseModel):
    id: Optional[int] = 0
    firstName: str
    lastName:  str
    cpf:       str
    brl:       float

class CreateAccountSchema(SchemaBaseModel):
    firstName: str
    lastName:  str
    cpf:       str
