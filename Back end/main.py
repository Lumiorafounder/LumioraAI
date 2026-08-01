from fastapi import FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
import uvicorn
from fastapi import Depends


from database import engine, Base, SessionLocal
from models import StudentDB, TeacherDB, AttendanceDB, FeesDB, SubjectDB, UserDB, MarksDB
from auth import (
    hash_password,
    verify_password,
    create_access_token,
    get_current_user,
    require_role
)

from auth import hash_password, verify_password
from jose import jwt
from auth import hash_password, verify_password


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


class Fees(BaseModel):
    id: int
    student_id: int
    amount: int
    month: str
    status: str


class Subject(BaseModel):
    id: int
    name: str
    teacher_id: int


class User(BaseModel):
    id: int
    username: str
    password: str
    role: str

class LoginRequest(BaseModel):
    username: str
    password: str


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

# ---------------- FEES APIs ----------------

@app.get("/fees")
def get_fees():
    db = SessionLocal()
    fees = db.query(FeesDB).all()
    db.close()
    return fees


@app.post("/fees")
def add_fee(fee: Fees):
    db = SessionLocal()

    new_fee = FeesDB(
        id=fee.id,
        student_id=fee.student_id,
        amount=fee.amount,
        month=fee.month,
        status=fee.status
    )

    db.add(new_fee)
    db.commit()
    db.close()

    return {
        "message": "Fee added successfully"
    }


@app.put("/fees/{fee_id}")
def update_fee(fee_id: int, fee: Fees):
    db = SessionLocal()

    db_fee = db.query(FeesDB).filter(
        FeesDB.id == fee_id
    ).first()

    if not db_fee:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Fee record not found"
        )

    db_fee.student_id = fee.student_id
    db_fee.amount = fee.amount
    db_fee.month = fee.month
    db_fee.status = fee.status

    db.commit()
    db.close()

    return {
        "message": "Fee updated successfully"
    }


@app.delete("/fees/{fee_id}")
def delete_fee(fee_id: int):
    db = SessionLocal()

    fee = db.query(FeesDB).filter(
        FeesDB.id == fee_id
    ).first()

    if not fee:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Fee record not found"
        )

    db.delete(fee)
    db.commit()
    db.close()

    return {
        "message": "Fee deleted successfully"
    }



# ---------------- SUBJECT APIs ----------------

@app.get("/subjects")
def get_subjects():
    db = SessionLocal()

    subjects = db.query(SubjectDB).all()

    db.close()

    return subjects


@app.post("/subjects")
def add_subject(subject: Subject):
    db = SessionLocal()

    new_subject = SubjectDB(
        id=subject.id,
        name=subject.name,
        teacher_id=subject.teacher_id
    )

    db.add(new_subject)
    db.commit()
    db.close()

    return {
        "message": "Subject added successfully"
    }


@app.put("/subjects/{subject_id}")
def update_subject(subject_id: int, subject: Subject):
    db = SessionLocal()

    db_subject = db.query(SubjectDB).filter(
        SubjectDB.id == subject_id
    ).first()

    if not db_subject:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Subject not found"
        )

    db_subject.name = subject.name
    db_subject.teacher_id = subject.teacher_id

    db.commit()
    db.close()

    return {
        "message": "Subject updated successfully"
    }

@app.delete("/subjects/{subject_id}")
def delete_subject(subject_id: int):
    db = SessionLocal()

    subject = db.query(SubjectDB).filter(
        SubjectDB.id == subject_id
    ).first()

    if not subject:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Subject not found"
        )

    db.delete(subject)
    db.commit()
    db.close()

    return {
        "message": "Subject deleted successfully"
    }

@app.get("/users")
def get_users():
    db = SessionLocal()
    users = db.query(UserDB).all()
    db.close()
    return users


@app.post("/register")
def register(user: User):
    db = SessionLocal()

    existing_user = db.query(UserDB).filter(
        UserDB.username == user.username
    ).first()

    if existing_user:
        db.close()
        raise HTTPException(
            status_code=400,
            detail="Username already exists"
        )

    new_user = UserDB(
        id=user.id,
        username=user.username,
        password=hash_password(user.password),
        role=user.role
    )

    db.add(new_user)
    db.commit()
    db.close()

    return {
        "message": "User registered successfully"
    }

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    db = SessionLocal()

    user = db.query(UserDB).filter(
        UserDB.username == form_data.username
    ).first()

    if not user:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if not verify_password(
        form_data.password,
        user.password
    ):
        db.close()
        raise HTTPException(
            status_code=401,
            detail="Invalid password"
        )

    token = create_access_token({
        "username": user.username,
        "role": user.role
    })

    db.close()

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@app.get("/admin/dashboard")
def admin_dashboard(
    current_user: dict = Depends(require_role("admin"))
):
    return {
        "message": "Welcome Admin",
        "user": current_user
    }


@app.post("/admin/fees")
def add_fees(
    current_user: dict = Depends(require_role("admin"))
):
    db = SessionLocal()

    fees = FeesDB(
        student_id=1,
        amount=50000,
        month="August",
        status="Pending"
    )

    db.add(fees)
    db.commit()
    db.refresh(fees)

    db.close()

    return {
        "message": "Fees added successfully",
        "id": fees.id
    }

@app.get("/teacher/dashboard")
def teacher_dashboard(
    current_user: dict = Depends(require_role("teacher"))
):
    return {
        "message": "Welcome Teacher",
        "user": current_user
    }


@app.get("/student/dashboard")
def student_dashboard(
    current_user: dict = Depends(require_role("student"))
):
    return {
        "message": "Welcome Student",
        "user": current_user
    }


@app.get("/student/attendance")
def student_attendance(
    current_user: dict = Depends(require_role("student"))
):
    db = SessionLocal()

    attendance = db.query(AttendanceDB).filter(
        AttendanceDB.student_id == 1
    ).all()

    db.close()

    return {
        "student": current_user["username"],
        "attendance": [
            {
                "date": item.date,
                "status": item.status
            }
            for item in attendance
        ]
    }

@app.get("/student/fees")
def student_fees(
    current_user: dict = Depends(require_role("student"))
):
    db = SessionLocal()

    fees = db.query(FeesDB).filter(
        FeesDB.student_id == 1
    ).all()

    db.close()

    return {
        "student": current_user["username"],
        "fees": [
            {
                "month": item.month,
                "amount": item.amount,
                "status": item.status
            }
            for item in fees
        ]
    }

@app.get("/student/subjects")
def student_subjects(
    current_user: dict = Depends(require_role("student"))
):
    return {
        "student": current_user["username"],
        "subjects": [
            {
                "name": "Mathematics",
                "teacher": "Ravi"
            },
            {
                "name": "Science",
                "teacher": "Anitha"
            }
        ]
    }

@app.get("/student/progress")
def student_progress(
    current_user: dict = Depends(require_role("student"))
):
    db = SessionLocal()

    marks = db.query(MarksDB).filter(
        MarksDB.student_id == 1
    ).all()

    db.close()

    return {
        "student": current_user["username"],
        "progress": [
            {
                "subject": item.subject,
                "marks": item.marks
            }
            for item in marks
        ]
    }

@app.get("/teacher/subjects")
def teacher_subjects(
    current_user: dict = Depends(require_role("teacher"))
):
    return {
        "teacher": current_user["username"],
        "subjects": [
            "Mathematics",
            "Science"
        ]
    }
@app.post("/teacher/attendance")
def mark_attendance(
    current_user: dict = Depends(require_role("teacher"))
):
    db = SessionLocal()

    attendance = AttendanceDB(
        student_id=1,
        date="2026-08-01",
        status="Present"
    )

    db.add(attendance)
    db.commit()
    db.refresh(attendance)

    db.close()

    return {
        "message": "Attendance saved successfully",
        "id": attendance.id
    }


@app.post("/teacher/marks")
def upload_marks(
    current_user: dict = Depends(require_role("teacher"))
):
    db = SessionLocal()

    marks = MarksDB(
        student_id=1,
        subject="Mathematics",
        marks=95
    )

    db.add(marks)
    db.commit()
    db.refresh(marks)

    db.close()

    return {
        "message": "Marks saved successfully",
        "id": marks.id
    }

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000
    )