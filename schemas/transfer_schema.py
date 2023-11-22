"""
    Structures to convert JSON into MODELs, MODELs into JSON
    and verify if there isn't any info missing
"""

from pydantic import BaseModel as SchemaBaseModel

class ValueSchema(SchemaBaseModel):
    value: float