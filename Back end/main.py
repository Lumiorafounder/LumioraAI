from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

from database import engine, Base
import models

app = FastAPI()

Base.metadata.create_all(bind=engine)

class Student(BaseModel):
    id: int
    name: str
    student_class: str


class Teacher(BaseModel):
    id: int
    name: str
    subject: str


students_db = []
teachers_db = []


@app.get("/")
def home():
    return {
        "message": "Welcome to Lumiora AI",
        "project": "AI Powered School ERP"
    }


@app.get("/students")
def get_students():
    return students_db


@app.post("/students")
def add_student(student: Student):
    students_db.append(student.model_dump())
    return {
        "message": "Student added successfully"
    }


@app.get("/teachers")
def get_teachers():
    return teachers_db


@app.post("/teachers")
def add_teacher(teacher: Teacher):
    teachers_db.append(teacher.model_dump())
    return {
        "message": "Teacher added successfully"
    }


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)