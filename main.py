from typing import Optional
from fastapi import FastAPI, Path
from pydantic import BaseModel

app = FastAPI()

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


class Student(BaseModel):
    name: str
    age: int
    year: str


class UpdateStudent(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    year: Optional[str] = None


@app.get("/")
def index():
    return {"name": "First Data"}


@app.get("/get-student/{student_id}")
def get_student(student_id: int = Path(..., description="The ID")):
    return students.get(student_id)


@app.get("/get-by-name")
def get_student(name: str):
    for item in students:
        if students[item]["name"] == name:
            return students[item]
    return {"data": "Not Found"}


@app.post("/create-student/{student_id}")
def create_student(student_id: int, student: Student):
    if student_id in students:
        return {"Error:" "Student exists"}

    students[student_id] = student
    return students[student_id]


@app.put("/update-student/{student_id}")
def update_student(student_id: int, student: UpdateStudent):
    if student_id not in students:
        return {"Error": "Student does not exist"}
    if student.name is not None:
        students[student_id].name = student.name
    if student.age is not None:
        students[student_id].age = student.age
    if student.year is not None:
        students[student_id].year = student.year

    return students[student_id]

@app.delete("/delete-student/{students_id}")
def delete_student(students_id: int):
    if students_id not in students:
        return {"Error","Student does not exist"}
    del students[students_id]
    return {"Massage", "Student Delete SuccessFull!"}