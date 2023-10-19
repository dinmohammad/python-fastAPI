from typing import Optional, Annotated
from fastapi import FastAPI, Path, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status

import models
from database import engine, SessionLocal

app = FastAPI()
# =====================================
models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
# ================================

students = {
    1: {
        "name": "Din",
        "age": 17,
        "class": "year 12"
    },
    10: {
        "name": "Jhon",
        "age": 30,
        "class": "year 30"
    }
}


class UserBase(BaseModel):
    username: str


class StudentBase(BaseModel):
    name: str
    age: int
    year: str


class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    year: Optional[str] = None


@app.post("/create_user/", status_code=status.HTTP_201_CREATED)
async def create_post(user: UserBase, db: db_dependency):
    db_user = models.User(**user.model_dump())
    db.add(db_user)
    db.commit()


@app.get("/")
def index():
    return {"name": "First Data"}


@app.post("/new_student/", status_code=status.HTTP_201_CREATED)
async def create_student(student: StudentBase, db: db_dependency):
    new_student = models.Student(**student.model_dump())
    db.add(new_student)
    db.commit()


@app.post("/new-student/{student_id}")
def create_student(student_id: int, db: db_dependency):
    existing_student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if existing_student:
        raise HTTPException(status_code=400, detail="Student already exists")
    new_student = models.Student(id=student_id)
    db.add(new_student)
    db.commit()


@app.get("/get-student/{student_id}")
def get_student(student_id: int, db: db_dependency):
    existing_student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if existing_student is None:
        raise HTTPException(status_code=400, detail="Student not found")
    return existing_student


@app.get("/get-all-student/", status_code=status.HTTP_200_OK)
def get_student(db: db_dependency):
    all_student = db.query(models.Student).all()
    if not all_student:
        raise HTTPException(status_code=400, detail="No student Data")
    return all_student


# @app.get("/get-by-name")
# def get_student(name: str):
#     for item in students:
#         if students[item]["name"] == name:
#             return students[item]
#     return {"data": "Not Found"}


@app.put("/update-student/{student_id}", status_code=status.HTTP_200_OK)
def update_student(student_id: int, db: db_dependency, student: StudentBase):
    existing_student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if not existing_student:
        raise HTTPException(status_code=400, detail="Student does not exist")
    existing_student.name = student.name
    existing_student.age = student.age
    existing_student.year = student.year
    db.commit()
    return HTTPException(status_code=200, detail="Student Update successfully")


@app.delete("/delete-student/{students_id}", status_code=status.HTTP_200_OK)
def delete_student(student_id: int, db: db_dependency):
    existing_student = db.query(models.Student).filter(models.Student.id == student_id).first()
    if existing_student is None:
        raise HTTPException(status_code=400, detail="Student does not exist")
    db.delete(existing_student)
    db.commit()
    return HTTPException(status_code=200, detail="Successfully Delete Student")
