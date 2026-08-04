from fastapi import FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
import uvicorn
from fastapi import Depends


from database import engine, Base, SessionLocal
from models import StudentDB, TeacherDB, AttendanceDB, FeesDB, SubjectDB, UserDB, MarksDB, ClassDB
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
    student_id: int
    date: str
    status: str

class Fees(BaseModel):
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

class Marks(BaseModel):
    student_id: int
    subject: str
    marks: int
class Class(BaseModel):
    class_name: str
    section: str
    teacher_id: int

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

    existing_student = db.query(StudentDB).filter(
        StudentDB.id == student_id
    ).first()

    if not existing_student:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    existing_student.name = student.name
    existing_student.student_class = student.student_class

    db.commit()
    db.refresh(existing_student)

    db.close()

    return {
        "message": "Student updated successfully",
        "student": existing_student
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
        "message": "Teacher added successfully"
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
        student_id=attendance.student_id,
        date=attendance.date,
        status=attendance.status
    )

    db.add(new_attendance)
    db.commit()
    db.refresh(new_attendance)
    db.close()

    return {
        "message": "Attendance added successfully",
        "id": new_attendance.id
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
def add_fees(fees: Fees):
    db = SessionLocal()

    new_fees = FeesDB(
        student_id=fees.student_id,
        amount=fees.amount,
        month=fees.month,
        status=fees.status
    )

    db.add(new_fees)
    db.commit()
    db.refresh(new_fees)
    db.close()

    return {
        "message": "Fees added successfully",
        "id": new_fees.id
    }


@app.put("/fees/{fees_id}")
def update_fees(fees_id: int, fees: Fees):
    db = SessionLocal()

    db_fees = db.query(FeesDB).filter(
        FeesDB.id == fees_id
    ).first()

    if not db_fees:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Fees not found"
        )

    db_fees.student_id = fees.student_id
    db_fees.amount = fees.amount
    db_fees.month = fees.month
    db_fees.status = fees.status

    db.commit()
    db.close()

    return {
        "message": "Fees updated successfully"
    }

@app.delete("/fees/{fees_id}")
def delete_fees(fees_id: int):
    db = SessionLocal()

    fees = db.query(FeesDB).filter(
        FeesDB.id == fees_id
    ).first()

    if not fees:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Fees not found"
        )

    db.delete(fees)
    db.commit()
    db.close()

    return {
        "message": "Fees deleted successfully"
    }



# ---------------- SUBJECT APIs ----------------

@app.get("/student/subjects")
def student_subjects(
    current_user: dict = Depends(require_role("student"))
):
    db = SessionLocal()

    subjects = db.query(SubjectDB).all()

    db.close()

    return {
        "student": current_user["username"],
        "subjects": [
            {
                "name": item.name,
                "teacher_id": item.teacher_id
            }
            for item in subjects
        ]
    }


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

@app.post("/admin/subjects")
def add_subject(
    current_user: dict = Depends(require_role("admin"))
):
    db = SessionLocal()

    subject = SubjectDB(
        name="Mathematics",
        teacher_id=1
    )

    db.add(subject)
    db.commit()
    db.refresh(subject)

    db.close()

    return {
        "message": "Subject added successfully",
        "id": subject.id
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
    marks: Marks,
    current_user: dict = Depends(require_role("teacher"))
):
    db = SessionLocal()

    new_marks = MarksDB(
        student_id=marks.student_id,
        subject=marks.subject,
        marks=marks.marks
    )

    db.add(new_marks)
    db.commit()
    db.refresh(new_marks)

    db.close()

    return {
        "message": "Marks saved successfully",
        "id": new_marks.id
        }
@app.get("/marks")
def get_marks():
    db = SessionLocal()

    marks = db.query(MarksDB).all()

    db.close()

    return marks


@app.put("/marks/{marks_id}")
def update_marks(marks_id: int, marks: Marks):
    db = SessionLocal()

    db_marks = db.query(MarksDB).filter(
        MarksDB.id == marks_id
    ).first()

    if not db_marks:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Marks not found"
        )

    db_marks.student_id = marks.student_id
    db_marks.subject = marks.subject
    db_marks.marks = marks.marks

    db.commit()
    db.close()

    return {
        "message": "Marks updated successfully"
    }

@app.delete("/marks/{marks_id}")
def delete_marks(marks_id: int):
    db = SessionLocal()

    marks = db.query(MarksDB).filter(
        MarksDB.id == marks_id
    ).first()

    if not marks:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Marks not found"
        )

    db.delete(marks)
    db.commit()
    db.close()

    return {
        "message": "Marks deleted successfully"
    }


@app.post("/classes")
def add_class(class_data: Class):
    db = SessionLocal()

    new_class = ClassDB(
        class_name=class_data.class_name,
        section=class_data.section,
        teacher_id=class_data.teacher_id
    )

    db.add(new_class)
    db.commit()
    db.refresh(new_class)
    db.close()

    return {
        "message": "Class added successfully",
        "id": new_class.id
    }

@app.get("/classes")
def get_classes():
    db = SessionLocal()

    classes = db.query(ClassDB).all()

    db.close()

    return classes


@app.put("/classes/{class_id}")
def update_class(class_id: int, class_data: Class):
    db = SessionLocal()

    db_class = db.query(ClassDB).filter(
        ClassDB.id == class_id
    ).first()

    if not db_class:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Class not found"
        )

        db_class.class_name = class_data.class_name
    db_class.section = class_data.section
    db_class.teacher_id = class_data.teacher_id

    db.commit()
    db.close()

    return {
        "message": "Class updated successfully"
    }


@app.delete("/classes/{class_id}")
def delete_class(class_id: int):
    db = SessionLocal()

    db_class = db.query(ClassDB).filter(
        ClassDB.id == class_id
    ).first()

    if not db_class:
        db.close()
        raise HTTPException(
            status_code=404,
            detail="Class not found"
        )

    db.delete(db_class)
    db.commit()
    db.close()

    return {
        "message": "Class deleted successfully"
    }
    
  
if __name__ == "__main__":
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000
    )