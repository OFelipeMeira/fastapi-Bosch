"""
    File from the model 'account'
"""

from core.configs import settings
from sqlalchemy import Column, Integer, String, Float

class AccountModel(settings.DBBaseModel):
    __tablename__ = "account"
    id:        int = Column(Integer, primary_key=True, autoincrement=True)
    firstName: str = Column(String(255))
    lastName:  str = Column(String(255))
    cpf:       str = Column(String(11))
    brl:       float = Column(Float(10,2))
