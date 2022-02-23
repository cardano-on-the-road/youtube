from unicodedata import name
from sqlalchemy.orm import Session

import models, schemas

def create_person(db: Session, person: schemas.PersonCreate):
    db_person = models.Person(name = person.name, age = person.age)
    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    return db_person

def get_person(db: Session, person_id: int):
    return db.query(models.Person).filter(models.Person.id == person_id).first()

def get_persons(db: Session):
    return db.query(models.Person).all() 