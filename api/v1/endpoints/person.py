from fastapi import APIRouter, status, HTTPException, Response
from database import models

router = APIRouter()

@router.get('/')
async def get_persons():
    return {'data': models.Person.all()}