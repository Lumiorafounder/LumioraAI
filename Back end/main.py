from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Student(BaseModel):
    id: int
    name: str
    student_class: str

@app.get("/")
def home():
    return {
        "message": "Welcome to Lumiora AI",
        "project": "AI Powered School ERP"
    }

@app.get("/students")
def get_students():
    return [
        {
            "id": 1,
            "name": "Aryan",
            "class": "2nd"
        },
        {
            "id": 2,
            "name": "Ananya",
            "class": "5th"
        }
    ]

@app.get("/teachers")
def get_teachers():
    return [
        {
            "id": 1,
            "name": "Ravi Kumar",
            "subject": "Mathematics"
        },
        {
            "id": 2,
            "name": "Lakshmi",
            "subject": "Science"
        }
    ]

@app.post("/students")
def add_student(student: Student):
    return {
        "message": "Student added successfully",
        "student": student
    }