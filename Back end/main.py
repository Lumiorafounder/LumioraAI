from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn

from database import engine, Base, SessionLocal
from models import StudentDB, TeacherDB, AttendanceDB


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


class Attendance(BaseModel):
    id: int
    student_id: int
    date: str
    status: str


@app.get("/")
def home():
    return {
        "message": "Welcome to Lumiora AI",
        "project": "AI Powered School ERP"
    }


# ---------------- STUDENT APIs ----------------

@app.get("/students")
def get_students():
    db = SessionLocal()
    students = db.query(StudentDB).all()
    db.close()
    return students


@app.post("/students")
def add_student(student: Student):
    db = SessionLocal()

    new_student = StudentDB(
        id=student.id,
        name=student.name,
        student_class=student.student_class
    )

    db.add(new_student)
    db.commit()
    db.close()

    return {
        "message": "Student added successfully to database"
    }


@app.put("/students/{student_id}")
def update_student(student_id: int, student: Student):
    db = SessionLocal()

    db_student = db.query(StudentDB).filter(
        StudentDB.id == student_id
    ).first()

    if not db_student:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    db_student.name = student.name
    db_student.student_class = student.student_class

    db.commit()
    db.close()

    return {
        "message": "Student updated successfully"
    }


@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    db = SessionLocal()

    student = db.query(StudentDB).filter(
        StudentDB.id == student_id
    ).first()

    if not student:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    db.delete(student)
    db.commit()
    db.close()

    return {
        "message": "Student deleted successfully"
    }


# ---------------- TEACHER APIs ----------------

@app.get("/teachers")
def get_teachers():
    db = SessionLocal()

    teachers = db.query(TeacherDB).all()

    db.close()

    return teachers


@app.post("/teachers")
def add_teacher(teacher: Teacher):
    db = SessionLocal()

    new_teacher = TeacherDB(
        id=teacher.id,
        name=teacher.name,
        subject=teacher.subject
    )

    db.add(new_teacher)
    db.commit()
    db.close()

    return {
        "message": "Teacher added successfully to database"
    }


@app.put("/teachers/{teacher_id}")
def update_teacher(teacher_id: int, teacher: Teacher):
    db = SessionLocal()

    db_teacher = db.query(TeacherDB).filter(
        TeacherDB.id == teacher_id
    ).first()

    if not db_teacher:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Teacher not found"
        )

    db_teacher.name = teacher.name
    db_teacher.subject = teacher.subject

    db.commit()
    db.close()

    return {
        "message": "Teacher updated successfully"
    }


@app.delete("/teachers/{teacher_id}")
def delete_teacher(teacher_id: int):
    db = SessionLocal()

    teacher = db.query(TeacherDB).filter(
        TeacherDB.id == teacher_id
    ).first()

    if not teacher:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Teacher not found"
        )

    db.delete(teacher)
    db.commit()
    db.close()

    return {
        "message": "Teacher deleted successfully"
    }

    # ---------------- ATTENDANCE APIs ----------------
# ---------------- ATTENDANCE APIs ----------------

@app.get("/attendance")
def get_attendance():
    db = SessionLocal()
    attendance = db.query(AttendanceDB).all()
    db.close()
    return attendance


@app.post("/attendance")
def add_attendance(attendance: Attendance):
    db = SessionLocal()

    new_attendance = AttendanceDB(
        id=attendance.id,
        student_id=attendance.student_id,
        date=attendance.date,
        status=attendance.status
    )

    db.add(new_attendance)
    db.commit()
    db.close()

    return {
        "message": "Attendance added successfully"
    }


@app.put("/attendance/{attendance_id}")
def update_attendance(attendance_id: int, attendance: Attendance):
    db = SessionLocal()

    db_attendance = db.query(AttendanceDB).filter(
        AttendanceDB.id == attendance_id
    ).first()

    if not db_attendance:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Attendance not found"
        )

    db_attendance.student_id = attendance.student_id
    db_attendance.date = attendance.date
    db_attendance.status = attendance.status

    db.commit()
    db.close()

    return {
        "message": "Attendance updated successfully"
    }


@app.delete("/attendance/{attendance_id}")
def delete_attendance(attendance_id: int):
    db = SessionLocal()

    attendance = db.query(AttendanceDB).filter(
        AttendanceDB.id == attendance_id
    ).first()

    if not attendance:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Attendance not found"
        )

    db.delete(attendance)
    db.commit()
    db.close()

    return {
        "message": "Attendance deleted successfully"
    }


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000
    )