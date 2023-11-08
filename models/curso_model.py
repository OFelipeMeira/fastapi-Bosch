"""
    File from the model 'curso'
"""

# To Test ------------------------------------------------------------------------- #
import sys                                                                          #
default_path = "C:\\Users\\CT67CA\\Desktop\\Temp Felipe DS6\\Python\\fastapi-Bosch" #
sys.path.append(default_path)                                                       #
# --------------------------------------------------------------------------------- # 

from core.configs import settings
from sqlalchemy import Column, Integer, String

class CursoModel(settings.DBBaseModel):
    __tablename__ = "curso"
    id:        int = Column(Integer, primary_key=True, autoincrement=True)
    titulo:    str = Column(String(100))
    instrutor: str = Column(String(100))
    horas:     int = Column(Integer)
    aulas:     int = Column(Integer)