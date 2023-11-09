"""

"""

from typing import Optional
from pydantic import BaseModel as SchemaBaseModel

class CursoSchema(SchemaBaseModel):
    id: Optional[int] = 0
    titulo:    str
    instrutor: str
    horas:     int
    aulas:     int
