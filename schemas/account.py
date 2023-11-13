from typing import Optional
from pydantic import BaseModel as SchemaBaseModel

class AccountSchema(SchemaBaseModel):
    id: Optional[int] = 0
    name: str
    cpf: str