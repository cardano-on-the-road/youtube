import string
from typing import Optional

from pydantic import BaseModel

class PersonCreate(BaseModel):
    name: str
    age: int

class Person(PersonCreate):
    id: int

    class Config():
        orm_mode = True