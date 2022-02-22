
from typing import Optional
from unicodedata import name

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from fastapi import FastAPI
from pydantic import BaseModel

SQLALCHEMY_DATABASE_URL = "postgresql://valerio.mellini@gmail.com:valeriopwd@localhost/pgdb"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

app = FastAPI()

class PersonDb(Base):
    __tablename__ = "persons"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    age = Column(Integer)


class Person(BaseModel):
    id:int
    name: str
    age: int


    
Base.metadata.create_all(engine)

def logger(msg):
    with open("log.txt", "a") as f:
        f.write(str(msg) + "\n")

@app.post("/persons/")
async def create_person(person: Person):
    logger(person)
    session = Session()
    session.add(PersonDb(id=person.id, name=person.name, age=person.age))
    session.commit()
    return person

@app.get("/persons/")
async def get_persons():
    session = Session()
    persons = session.query(PersonDb).all()
    logger(persons)
    return persons

